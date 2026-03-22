text
# Installation de pi-slideshow sur Raspberry Pi (Bullseye)

## 0. Pré‑requis

- Raspberry Pi OS **Bullseye** (testé avec 2022).  
- Wi‑Fi configuré.  
- SSH activé.

Vérification de la version de l’OS :

```bash
lsb_release -a
Exemple attendu :

text
Distributor ID: Raspbian
Description:    Raspbian GNU/Linux 11 (bullseye)
Release:        11
Codename:       bullseye
Remarque : Buster n’a plus de dépôts publics permettant l’installation de Docker (au 22/03/2026), il est donc déconseillé pour cette installation.

1. Créer l’utilisateur dédié
Connecté en pi (ou un autre utilisateur admin) :

bash
sudo adduser slideshow
Choisissez un mot de passe pour slideshow.

Les autres questions (Nom, etc.) peuvent être laissées vides (Entrée).

Optionnel : ajouter l’utilisateur au groupe sudo pour lui donner des droits d’administration :

bash
sudo usermod -aG sudo slideshow
2. Activer l’auto‑login graphique pour cet utilisateur
Lancez raspi-config :

bash
sudo raspi-config
Dans les menus :

System Options (ou System selon la version).

Boot / Auto Login.

Choisir Desktop Autologin (auto‑login sur l’interface graphique).

Pour que ce soit l’utilisateur slideshow qui se connecte automatiquement, éditez ensuite la configuration de LightDM :

bash
sudo nano /etc/lightdm/lightdm.conf
Cherchez la section [Seat:*] et ajoutez/modifiez ces lignes (ou décommentez‑les) :

text
[Seat:*]
autologin-user=slideshow
autologin-user-timeout=0
Enregistrez (Ctrl+O, Entrée) puis quittez (Ctrl+X), et redémarrez :

bash
sudo reboot
Après reboot, vous devez arriver directement sur le bureau en tant que slideshow (et non plus pi).

3. Installer Docker sur le Raspberry Pi
Ouvrez un terminal (toujours sur le Pi) :

bash
sudo apt update
sudo apt upgrade -y
Installez Docker avec le script officiel :

bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
Ajoutez ensuite l’utilisateur slideshow au groupe docker pour pouvoir lancer les containers sans sudo :

bash
sudo usermod -aG docker slideshow
Déconnectez‑vous / reconnectez‑vous (ou redémarrez) pour que le groupe soit pris en compte.

Vérifiez que Docker fonctionne :

bash
docker run hello-world
Vous devez voir un message « Hello from Docker! ».

4. Cloner le dépôt pi‑slideshow
Connecté en tant que slideshow :

bash
cd ~
git clone https://github.com/JMSrulez/pi-slideshow.git
cd pi-slideshow
5. Construire et lancer le container
Depuis le dossier ~/pi-slideshow :

bash
docker build -t pi-slideshow .
Sur un Raspberry Pi, la construction peut prendre plusieurs minutes (par exemple ~10 minutes, le temps d’un café).

Lancez ensuite l’application :

bash
docker run -d \
  --name pi-slideshow \
  -p 5000:5000 \
  -v /home/slideshow:/home/slideshow \
  -e PI_SLIDESHOW_TITLE="Pi Slideshow - Écran 1" \
  pi-slideshow
L’application sera accessible sur :
http://<ip_du_pi>:5000 (par exemple http://192.168.1.42:5000).

Les vidéos générées seront écrites dans /home/slideshow sur le Pi (ce chemin peut être adapté en modifiant l’option -v et la configuration de l’application).

À partir d’ici, vous pouvez ouvrir l’interface web depuis un autre appareil du réseau, uploader des images et générer le diaporama vidéo.

text

Tu peux enregistrer ce contenu dans `SETUP.md` à la racine du repo. Tu veux qu’on ajoute juste après une section “Mode kiosk VLC (optionnel)” qui explique l’installation de `vlc-kiosk.sh` et du service systemd, ou tu préfères séparer ça dans un autre fichier type `KIOSK.md` ?
