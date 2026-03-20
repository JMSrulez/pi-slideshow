#!/bin/bash
# Script exemple pour lancer VLC en mode kiosk sur un Raspberry Pi

VIDEO_PATH="${VIDEO_PATH:-/home/pi/video_pi3_photos.mp4}"
DISPLAY_VALUE="${DISPLAY_VALUE:-:0}"

export DISPLAY="$DISPLAY_VALUE"

# laisser le temps à la session graphique de démarrer
sleep 10

# Attendre que la vidéo existe et ne soit pas vide
while [ ! -s "$VIDEO_PATH" ]; do
  sleep 1
done

/usr/bin/vlc -Rf \
  --vout=x11 \
  --loop \
  --quiet \
  --no-video-title-show \
  --avcodec-hw none \
  --no-osd \
  --no-qt-error-dialogs \
  "$VIDEO_PATH" vlc://quit
