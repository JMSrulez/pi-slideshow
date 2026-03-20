# pi-slideshow

Petit serveur Flask + Docker pour créer un diaporama vidéo à partir d'images
et le diffuser en mode kiosk sur un Raspberry Pi 3B+
Utilise ffmpeg pour generer de video de 1 à 60s et ensuite concatene l'ensemble, l'object est de ne pas saturer les 1Go RAM.

## Contenu

- `app.py` : application Flask
- `templates/index.html` : interface web
- `Dockerfile` : image Docker
- `requirements.txt` : dépendances Python

```bash
VLC Kiosk mode is a quick way to display video on raspberry pi in loop from existing file into home directory of the auto loggin user
It is just a basic linux service running a vlc command line to main display. You can follow instruction into script and systemd folder.
```
## Warning !

path to video is hardcoded at the moment...
As pi is intended to run as kiosk mode and autologin, may be the file in home directory of docker user might be best one.
For sure I will add as docker parameter

## Démarrage rapide

```bash
docker build -t picshow:latest .
docker run --rm -p 5000:5000 -v /home/pi:/home/pi picshow:latest

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

L'application elle meme tiens dans ces 2 fichiers app.py et index.html, docker est optionel mais pratique car il contiens les bon module python.

## Docker
Depuis le dossier :~/pi-slideshow  
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
