## Installer le service systemd  

```bash
sudo cp systemd/mpv-kiosk.service /etc/systemd/system/mpv-kiosk.service
sudo systemctl daemon-reload
sudo systemctl enable --now mpv-kiosk.service
```

Adaptez dans /etc/systemd/system/mpv-kiosk.service les lignes :

```bash
User=pi
Group=pi
Environment=DISPLAY=:0
Environment=VIDEO_PATH=/home/pi/video_pi3_photos.mp4
```
