## Installer le service systemd  

```bash
sudo cp systemd/mpv-kiosk.service /etc/systemd/system/mpv-kiosk.service
sudo systemctl daemon-reload
sudo systemctl enable --now mpv-kiosk.service
```

An example of a situation to know the groups and the id
```bash
~/pi-slideshow $ id
uid=1001(slideshow) gid=1001(slideshow) groupes=1001(slideshow),27(sudo),995(docker)
```

Adapt the lines in /etc/systemd/system/mpv-kiosk.service:
```bash
User=slideshow
Group=slideshow
Environment=DISPLAY=:0
Environment=VIDEO_PATH=/home/slideshow/video_pi3_photos.mp4
Environment=XDG_RUNTIME_DIR=/run/user/1001
```
