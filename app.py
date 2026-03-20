import os
from datetime import datetime
from flask import Flask, request, render_template, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import subprocess

from threading import Lock

generate_lock = Lock()
is_generating = False

APP_TITLE = os.environ.get("PI_SLIDESHOW_TITLE", "Pi Slideshow")
VIDEO_PATH = "/home/dlp/video_pi3_photos.mp4"
UPLOAD_FOLDER = "/tmp/uploads"          # interne au container
OUTPUT_VIDEO = "/home/dlp/video_pi3_photos.mp4"
ALLOWED_EXT = {"png", "jpg", "jpeg"}


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/video")
def video_file():
    if not os.path.exists(VIDEO_PATH):
        return "", 404
    return send_file(VIDEO_PATH, mimetype="video/mp4")

@app.route("/video_info")
def video_info():
    if not os.path.exists(VIDEO_PATH):
        return jsonify({"exists": False})
    st = os.stat(VIDEO_PATH)
    size = st.st_size
    mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "exists": True,
        "size": size,
        "mtime": mtime,
    })

@app.route("/")
def index():
    files = sorted(os.listdir(UPLOAD_FOLDER))
    return render_template("index.html", files=files, app_title=APP_TITLE)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/upload", methods=["POST"])
def upload():
    uploaded = []
    for f in request.files.getlist("files"):
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            path = os.path.join(UPLOAD_FOLDER, fname)
            f.save(path)
            uploaded.append(fname)
    return jsonify({"files": uploaded})

@app.route("/generate", methods=["POST"])
def generate():
    global is_generating

    # empêche plusieurs générations en parallèle
    if not generate_lock.acquire(blocking=False):
        return jsonify({"error": "generation already running"}), 409
    if is_generating:
        generate_lock.release()
        return jsonify({"error": "generation already running"}), 409
    is_generating = True

    try:
        data = request.get_json()
        items = data.get("items", [])
        if not items:
            is_generating = False
            generate_lock.release()
            return jsonify({"error": "no items"}), 400

        tmp_dir = "/tmp/picshow_segments"
        os.makedirs(tmp_dir, exist_ok=True)

        segment_paths = []
        total = len(items)
        current = 0

        # 1) génération 1 image = 1 vidéo
        for item in items:
            fname = item["file"]
            dur = max(1, min(60, int(item.get("duration", 3))))  # 1–60 s
            img_path = os.path.join(UPLOAD_FOLDER, fname)

            seg_name = f"seg_{current:04d}.mp4"
            seg_path = os.path.join(tmp_dir, seg_name)
            # on écrase systématiquement le segment
            if os.path.exists(seg_path):
                os.remove(seg_path)

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-t", str(dur), "-i", img_path,
                "-vf",
                "scale=1280:720:force_original_aspect_ratio=decrease,"
                "pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-threads", "1",
                seg_path,
            ]

            print(f"[picshow] ffmpeg segment {current+1}/{total}:", " ".join(cmd), flush=True)

            proc = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            if proc.returncode != 0:
                print("FFmpeg segment error:", proc.stderr, flush=True)
                is_generating = False
                generate_lock.release()
                return jsonify({
                    "error": "ffmpeg segment failed",
                    "detail": proc.stderr,
                    "step": "segment",
                    "index": current,
                }), 500

            segment_paths.append(seg_path)
            current += 1

        # 2) concaténation des segments
        list_file = os.path.join(tmp_dir, "segments.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for p in segment_paths:
                # chemin échappé pour ffmpeg concat demuxer
                f.write(f"file '{p}'\n")

        tmp_video = "/home/dlp/video_pi3_photos.tmp.mp4"
        final_video = "/home/dlp/video_pi3_photos.mp4"

        if os.path.exists(tmp_video):
            os.remove(tmp_video)

        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            tmp_video,
        ]
        print("[picshow] ffmpeg concat:", " ".join(concat_cmd), flush=True)

        proc2 = subprocess.run(
            concat_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if proc2.returncode != 0:
            print("FFmpeg concat error:", proc2.stderr, flush=True)
            if os.path.exists(tmp_video):
                os.remove(tmp_video)
            is_generating = False
            generate_lock.release()
            return jsonify({
                "error": "ffmpeg concat failed",
                "detail": proc2.stderr,
                "step": "concat",
            }), 500

        # remplacement atomique du fichier final
        os.replace(tmp_video, final_video)

        st = os.stat(final_video)
        size = st.st_size
        mtime = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        is_generating = False
        generate_lock.release()

        return jsonify({
            "status": "ok",
            "size": size,
            "mtime": mtime,
            "segments": total,
        })

    except Exception as e:
        print("Exception during generation:", str(e), flush=True)
        if os.path.exists("/home/dlp/video_pi3_photos.tmp.mp4"):
            os.remove("/home/dlp/video_pi3_photos.tmp.mp4")
        is_generating = False
        generate_lock.release()
        return jsonify({"error": str(e)}), 500

@app.route("/delete", methods=["POST"])
def delete_file():
    data = request.get_json()
    fname = data.get("file")
    if not fname:
        return jsonify({"error": "no file"}), 400
    path = os.path.join(UPLOAD_FOLDER, fname)
    try:
        if os.path.exists(path):
            os.remove(path)
        return jsonify({"status": "ok"})
    except OSError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_all", methods=["POST"])
def delete_all():
    try:
        for name in os.listdir(UPLOAD_FOLDER):
            path = os.path.join(UPLOAD_FOLDER, name)
            if os.path.isfile(path):
                os.remove(path)
        return jsonify({"status": "ok"})
    except OSError as e:
        return jsonify({"error": str(e)}), 500
