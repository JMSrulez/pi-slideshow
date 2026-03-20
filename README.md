# pi-slideshow

Petit serveur Flask + Docker pour créer un diaporama vidéo à partir d'images
et le diffuser en mode kiosk sur un Raspberry Pi 3B+
Utilise ffmpeg pour generer de video de 1 à 60s et ensuite concatene l'ensemble, l'object est de ne pas saturer les 1Go RAM.

## Contenu

- `app.py` : application Flask
- `templates/index.html` : interface web
- `Dockerfile` : image Docker
- `requirements.txt` : dépendances Python

## Démarrage rapide

```bash
docker build -t pi-slideshow .
docker run --rm -p 5000:5000 -v /home/dlp:/home/dlp pi-slideshow

environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5000
      - PI_SLIDESHOW_TITLE=Lobby TV slideshow
