## Mode kiosk VLC (exemple Raspberry Pi)

### 1. Installer le script

```bash
sudo cp scripts/vlc-kiosk.sh /usr/local/bin/vlc-kiosk.sh
sudo chmod +x /usr/local/bin/vlc-kiosk.sh
```

Vous pouvez personnaliser le chemin de la vidéo et le display via les
variables d’environnement VIDEO_PATH et DISPLAY_VALUE dans le
fichier ou via le service systemd.

Le raspberry pi utiliser pour teste et developper est un pi 3B+, j'ai mis une résoltion des video raisonable 1280:720 pour eviter les lag.
la pauvre machine à du mal à afficher des video HD.
Le pi 3B+ ne coutant pas plus de 20 à 30$, cela fait une solution local déconnecté d'internet (si besoin) à bas prix.

