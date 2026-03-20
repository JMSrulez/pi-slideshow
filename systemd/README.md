 Installer le service systemd

** bash

sudo cp systemd/vlc-kiosk.service /etc/systemd/system/vlc-kiosk.service
sudo systemctl daemon-reload
sudo systemctl enable --now vlc-kiosk.service

Adaptez dans /etc/systemd/system/vlc-kiosk.service les lignes :

** text
 - User=pi
 - Group=pi
 - Environment=DISPLAY=:0
 - Environment=VIDEO_PATH=/home/pi/video_pi3_photos.mp4
