#!/bin/bash
# Kiosk script for mpv on Raspberry Pi 
# plays the video in full screen loop 
# when the video changes, kill mpv and exit so that systemd restarts the service

VIDEO_PATH="${VIDEO_PATH:-/home/slideshow/video_pi3_photos.mp4}"
DISPLAY_VALUE="${DISPLAY_VALUE:-:0}"

export DISPLAY="$DISPLAY_VALUE"

VIDEO_DIR="$(dirname "$VIDEO_PATH")"
VIDEO_FILE="$(basename "$VIDEO_PATH")"

# Let it open desktop
sleep 3

# Wait for an existing file
while [ ! -s "$VIDEO_PATH" ]; do
  sleep 1
done

# Launch mpv in background
/usr/bin/mpv \
  --fs \
  --loop=inf \
  --no-osd-bar \
  --no-input-default-bindings \
  --no-terminal \
  --really-quiet \
  "$VIDEO_PATH" &
MPV_PID=$!

# Wait file or folder event
read DIR EVENT NAME < <(inotifywait -q -e close_write,move,create,delete --format '%w %e %f' "$VIDEO_DIR")

if [ "$NAME" = "$VIDEO_FILE" ]; then
  # Le fichier vidéo a changé -> tuer mpv et sortir
  kill "$MPV_PID" 2>/dev/null
  wait "$MPV_PID" 2>/dev/null
fi

# Exit in a clean way, the service will relaunch the script
exit 0
