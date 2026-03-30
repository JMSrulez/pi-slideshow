# pi-slideshow

Small Flask + Docker server to create a video slideshow from images and stream it in kiosk mode on a Raspberry Pi 3B+.  
Use ffmpeg to generate a video from 1 to 60s and then concatenate everything, the objective is not to saturate the 1Go RAM.

This is not a copy of https://github.com/adafruit/pi_video_looper, this is a fully orginal video maker and looper design for non-IT end users.
Web interface is ultra simple, user upload jpeg, png, and generate presentation that is display in loop automaticaly. 
You, as IT guy will have to setup services and docker image.

## Content

- `app.py` : Flask application
- `templates/index.html` : web interface
- `Dockerfile` : Docker image
- `requirements.txt` : Python dependency

```bash
MPV Kiosk mode (could be VLC) is a quick way to display video on raspberry pi in loop from existing file into home directory of the auto loggin user. It is just a basic linux service running a mpv command line to main display. You can follow instruction into script and systemd folder.
```
## Warning !

As pi is intended to run as kiosk mode and autologin, I choose video file location in home directory of docker user might be best one.
You can customize at docker env parameter.  

## Quick Start

```bash
docker build -t picshow:latest .
docker run --rm -p 5000:5000 -v /home/slideshow:/home/slideshow picshow:latest

environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5000
      - PI_SLIDESHOW_TITLE=Lobby TV slideshow
```
---
## Architecture
pi@myhost:~/pi-slideshow $ tree
.  
├── app.py  
└── templates  
    └── index.html  

The application itself fits into these 2 app.py and index.html files, docker is optional but practical because it contains the right python module.  

## Docker
From folder :~/pi-slideshow  
├── Dockerfile  
├── requirements.txt  

```bash
docker build -t picshow:latest .
```

Deploy your container  
├── compose.yml
```bash
docker compose -f compose.yml up -d
```
