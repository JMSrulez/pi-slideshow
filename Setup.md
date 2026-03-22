# Installation de pi-slideshow sur Raspberry Pi (Bullseye)

## Overview
Pi Slideshow is a simple photo slideshow program for the Raspberry Pi. This guide will help you install and run the application quickly and effectively.
To run on Raspberry PI 3B+ version and code have been adjusted, so you can use cheap refurbished legacy rasperry pi.

0. **Pré‑requis**
- Raspberry Pi OS **Bullseye** 
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
Ouvrez un terminal (toujours sur le Pi) :
   ```bash
sudo apt update
sudo apt upgrade -y
   ```
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

