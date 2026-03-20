## Mode kiosk VLC (exemple Raspberry Pi)

### 1. Installer le script

```bash
sudo cp scripts/vlc-kiosk.sh /usr/local/bin/vlc-kiosk.sh
sudo chmod +x /usr/local/bin/vlc-kiosk.sh
```

Vous pouvez personnaliser le chemin de la vidéo et le display via les
variables d’environnement VIDEO_PATH et DISPLAY_VALUE dans le
fichier ou via le service systemd.

Le raspberry pi utiliser pour teste et developper est un pi 3B+, j'ai mis une résoltion des video raisonable pour eviter les lag.

