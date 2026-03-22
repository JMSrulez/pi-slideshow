# Installation de pi-slideshow sur Raspberry Pi (Bullseye)

## Overview
Pi Slideshow is a simple photo slideshow program for the Raspberry Pi. This guide will help you install and run the application quickly and effectively.

## 0. Pré‑requis
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
