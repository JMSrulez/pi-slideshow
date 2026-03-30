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

You can customize the video path and display via the VIDEO_PATH and DISPLAY_VALUE environment variables in the file or via the systemd service.

### 2. Limitation
The raspberry pi used to test and develop is a 3B+ pi with 1GB of RAM, I set a reasonable video resolution of 1280x720 to avoid lag. the poor machine has difficulty displaying HD videos.
The pi 3B+ costs no more than $20 to $30, making it an autonomous local solution disconnected from the internet (if necessary) at a low price.

### 3. Comments
Dockerize mpv is not recommended, it is very difficult to go from a docker to the remote display (it remains possible, but greedy), I abandoned the idea and in any case it is independent of the generator slide show. you just need to have the path of the file to project in common. 

