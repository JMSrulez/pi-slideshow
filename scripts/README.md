## Mode kiosk VLC (exemple Raspberry Pi)

### 1. Installer le script

```bash
sudo cp scripts/vlc-kiosk.sh /usr/local/bin/vlc-kiosk.sh
sudo chmod +x /usr/local/bin/vlc-kiosk.sh
```

Vous pouvez personnaliser le chemin de la vidéo et le display via les
variables d’environnement VIDEO_PATH et DISPLAY_VALUE dans le
fichier ou via le service systemd.

### 2. Limitation
Le raspberry pi utiliser pour teste et developper est un pi 3B+, j'ai mis une résoltion des video raisonable 1280x720 pour eviter les lag.
la pauvre machine à du mal à afficher des video HD.
Le pi 3B+ ne coutant pas plus de 20 à 30$, cela fait une solution local autonome déconnecté d'internet (si besoin) à bas prix.

### 3. Commentaire
Dockeriser VLC n'est pas conseillé, c'est très penible de passer d'un docker à l'affichage distant (ça reste possible, mais gourmand), j'ai abandonné l'idée et de toute facon c'est indépendant du générateur de slide show. il faut juste avoir le chemin du fichier à projeter en commun. 

