# pi-slideshow

Petit serveur Flask + Docker pour créer un diaporama vidéo à partir d'images
et le diffuser en mode kiosk sur un Raspberry Pi.

## Contenu

- `app.py` : application Flask
- `templates/index.html` : interface web
- `Dockerfile` : image Docker
- `requirements.txt` : dépendances Python

## Démarrage rapide

```bash
docker build -t pi-slideshow .
docker run --rm -p 5000:5000 -v /home/dlp:/home/dlp pi-slideshow
