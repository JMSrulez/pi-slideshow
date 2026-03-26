## Mode kiosk MPV (exemple Raspberry Pi)
you can try vlc but I switched to mpv dur to issues with video stack of x11 and MMAL

for this installation user must be sudoer but it is not mandatory to use the slideshow user.
### 0. Prerequis
Le user "slideshow" doit etre en autologin pour le mode kiosk
```bash
sudo nano /etc/lightdm/lightdm.conf

changer les lignes suivante :

#autologin-guest=false
autologin-user=slideshow
autologin-user-timeout=0
#autologin-in-background=false
```


### 1. Installer le script

```bash
sudo apt install -y mpv inotify-tools
sudo cp scripts/mpv-kiosk.sh /usr/local/bin/mpv-kiosk.sh
sudo chmod +x /usr/local/bin/mpv-kiosk.sh
```

Vous pouvez personnaliser le chemin de la vidéo et le display via les
variables d’environnement VIDEO_PATH et DISPLAY_VALUE dans le
fichier ou via le service systemd.

### 2. Limitation
Le raspberry pi utilisé pour teste et developper est un pi 3B+ avec 1Go de RAM, j'ai mis une résoltion des video raisonable 1280x720 pour eviter les lag. la pauvre machine à du mal à afficher des video HD.
Le pi 3B+ ne coutant pas plus de 20 à 30$, cela fait une solution local autonome déconnecté d'internet (si besoin) à bas prix.

### 3. Commentaire
Dockeriser mpv n'est pas conseillé, c'est très penible de passer d'un docker à l'affichage distant (ça reste possible, mais gourmand), j'ai abandonné l'idée et de toute facon c'est indépendant du générateur de slide show. il faut juste avoir le chemin du fichier à projeter en commun. 

