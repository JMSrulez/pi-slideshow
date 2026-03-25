# Installation de pi-slideshow sur Raspberry Pi (Bullseye)

## Overview
Pi Slideshow is a simple photo slideshow program for the Raspberry Pi. This guide will help you install and run the application quickly and effectively.
To run on Raspberry PI 3B+ version process have been adjusted, so you can use cheap refurbished legacy rasperry pi.

0. **Pré‑requis**
- Raspberry Pi OS **Bullseye** (use latest version on RPi 4 or 5)
- Wi‑Fi configuré.  
- SSH activé.

## Installation Steps

1. **Créer l’utilisateur dédié**
Connecté en pi (ou un autre utilisateur admin) :
 ```bash
sudo adduser slideshow
 ```
Choisissez un mot de passe pour slideshow.
Les autres questions (Nom, etc.) peuvent être laissées vides (Entrée).

Optionnel : ajouter l’utilisateur au groupe sudo pour lui donner des droits d’administration :
 ```bash
sudo usermod -aG sudo slideshow
 ```

2. **Update the Package List**  
Run the following command to ensure all your packages are up-to-date:
```bash
sudo apt update
sudo apt upgrade
```

3. **Installer Docker sur le Raspberry Pi**  
Installez Docker avec le script officiel :  
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Ajoutez ensuite l’utilisateur slideshow au groupe docker pour pouvoir lancer les containers sans sudo :
   ```bash
sudo usermod -aG docker slideshow
   ```
Déconnectez‑vous / reconnectez‑vous (ou redémarrez) pour que le groupe soit pris en compte.

Vérifiez que Docker fonctionne :

   ```bash
docker run hello-world
   ```
Vous devez voir un message « Hello from Docker! ».

4. **Cloner le dépôt pi‑slideshow**
Connecté en tant qu'utilisateur slideshow :

  ```bash
cd ~
git clone https://github.com/JMSrulez/pi-slideshow.git
cd pi-slideshow
  ```

5. **Construire et lancer le container**
Depuis le dossier ~/pi-slideshow :
  ```bash
docker build -t pi-slideshow .
  ```
Sur un Raspberry Pi, la construction peut prendre plusieurs minutes (par exemple ~10 minutes, testé sur une install fraiche à 596s).

Lancez ensuite l’application :

   ```bash
docker run -d \
  --name pi-slideshow \
  -p 5000:5000 \
  -v /home/slideshow:/home/slideshow \
  -e PI_SLIDESHOW_TITLE="Pi Slideshow - Écran 1" \
  pi-slideshow
   ```

L’application sera accessible sur :
http://<ip_du_pi>:5000 (par exemple http://192.168.1.42:5000).

6. **Exemple de script pour afficher la video généré en boucle**
Copier le script exemple dans /usr/local/bin :
  ```bash
sudo cp scripts/mpv-kiosk.sh /usr/local/bin/mpv-kiosk.sh
  ```
Rendre le script exécutable :
  ```bash
sudo chmod +x /usr/local/bin/mpv-kiosk.sh
  ```
Vérifier ou adapter les variables du script

Ouvrir le script avec un éditeur de texte :
```bash
sudo nano /usr/local/bin/mpv-kiosk.sh
```

Vérifier les lignes suivantes au début du fichier :
  ```bash
VIDEO_PATH="${VIDEO_PATH:-/home/slideshow/video_pi3_photos.mp4}"
DISPLAY_VALUE="${DISPLAY_VALUE:-:0}"
  ```
VIDEO_PATH : chemin complet de la vidéo générée par pi-slideshow.
Par défaut : /home/slideshow/video_pi3_photos.mp4

DISPLAY_VALUE : display X11 utilisé par la session graphique.
Sur un Raspberry Pi classique : :0

7. **Creer un service pour lancer MPV au démmarage**  

Copier le service dans /etc/systemd/system  
Depuis le dossier du projet :
  ```bash
cd ~/pi-slideshow
sudo cp systemd/mpv-kiosk.service /etc/systemd/system/mpv-kiosk.service
  ```
Adapter l’utilisateur et le chemin vidéo  
Éditer le fichier de service :
  ```bash
sudo nano /etc/systemd/system/mpv-kiosk.service
  ```
Vérifier et adapter ces lignes :
  ```bash
[Service]
User=slideshow
Group=slideshow
Environment=DISPLAY=:0
Environment=VIDEO_PATH=/home/slideshow/video_pi3_photos.mp4
ExecStart=/usr/local/bin/vlc-kiosk.sh
Restart=always
RestartSec=5
  ```
User / Group : l’utilisateur qui ouvre la session graphique (par exemple slideshow).

DISPLAY : doit correspondre au display de la session X (en général :0).

VIDEO_PATH : doit être le même que dans le script, et pointer sur la vidéo générée par pi-slideshow.

Recharger systemd et activer le service
Exécuter :
  ```bash
sudo systemctl daemon-reload
sudo systemctl enable --now vlc-kiosk.service
  ```
Vérifier le fonctionnement
Vérifier l’état du service :
  ```bash
systemctl status vlc-kiosk.service
  ```
Le service doit être “active (running)”.

Si une vidéo valide existe déjà à l’emplacement VIDEO_PATH, VLC doit démarrer et l’afficher en boucle sur l’écran connecté au Raspberry Pi.

En cas de problème, consulter les logs :
  ```bash
journalctl -u mpv-kiosk.service -e
  ```
Fonctionnement avec pi-slideshow
L’application pi-slideshow (dans Docker) écrit la vidéo finale dans le fichier configuré dans VIDEO_PATH (par défaut : /home/slideshow/video_pi3_photos.mp4).

Le script vlc-kiosk.sh attend que ce fichier existe et ait une taille non nulle, puis lance VLC en boucle dessus.

Quand une nouvelle vidéo est générée par pi-slideshow (fichier remplacé de manière atomique), VLC redémarre automatiquement au prochain problème de lecture ou lors d’un redémarrage du service, et diffuse la nouvelle version.
