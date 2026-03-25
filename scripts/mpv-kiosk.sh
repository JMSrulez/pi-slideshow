#!/bin/bash
# Script kiosk pour mpv sur Raspberry Pi
# - lit la vidéo en boucle plein écran
# - quand la vidéo change, tue mpv et sort pour que systemd relance le service

VIDEO_PATH="${VIDEO_PATH:-/home/dlp/video_pi3_photos.mp4}"
DISPLAY_VALUE="${DISPLAY_VALUE:-:0}"

export DISPLAY="$DISPLAY_VALUE"

VIDEO_DIR="$(dirname "$VIDEO_PATH")"
VIDEO_FILE="$(basename "$VIDEO_PATH")"

# Laisser le temps à la session graphique de démarrer
sleep 3

# Attendre que la vidéo existe et ne soit pas vide
while [ ! -s "$VIDEO_PATH" ]; do
  sleep 1
done

# Lancer mpv en arrière-plan
/usr/bin/mpv \
  --fs \
  --loop=inf \
  --no-osd-bar \
  --no-input-default-bindings \
  --no-terminal \
  --really-quiet \
  "$VIDEO_PATH" &
MPV_PID=$!

# Attendre UN événement sur le dossier, puis vérifier que c'est bien le bon fichier
read DIR EVENT NAME < <(inotifywait -q -e close_write,move,create,delete --format '%w %e %f' "$VIDEO_DIR")

if [ "$NAME" = "$VIDEO_FILE" ]; then
  # Le fichier vidéo a changé -> tuer mpv et sortir
  kill "$MPV_PID" 2>/dev/null
  wait "$MPV_PID" 2>/dev/null
fi

# Sortir : systemd relancera le service (et donc un nouveau mpv sur la nouvelle vidéo)
exit 0
