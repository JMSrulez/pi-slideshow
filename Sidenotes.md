
## Cloudflare
To remote control from internet your slideshow :

I use cloudflare, however latest version are not anymore available, I dig the web to find following docker repo.

erisamoe/cloudflared: A simple Alpine-based image supporting multiple architectures including linux/arm/v7 (32-bit) and linux/arm64 (64-bit). 
crazymax/cloudflared: A multi-arch image specifically noted for supporting ARM devices like Raspberry Pi. 
milgradesec/cloudflared: A modified image designed to run as a limited user, available on Docker Hub and GitHub Container Registry

## Basic routing to setup new raspberry PI
As Wifi is setup first boot, you may get ip from command
* ip a

Run raspi-config then
* update Hostname,
* expand file system
* switch off screen blanking (important for kiosk mode)
* activate ssh

