# pi-setup [![Build Status](https://travis-ci.org/creative-workflow/pi-setup.svg)](https://travis-ci.org/creative-workflow/pi-setup) [![Code Climate](https://codeclimate.com/github/creative-workflow/pi-setup/badges/gpa.svg)](https://codeclimate.com/github/creative-workflow/pi-setup)

## fabric usage
call `fab` to see a list of all available commands and options
call `fab pi:[your pi-ip] run:"ls -al"` to execute a command
if you setup you config.yml proper you can also run `fab pi run:"ls -al"`
setup/start/stop a service local or remote with `fab [service]:[command]` if you are on the pi or `fab pi:[your pi-ip] [service]:[command]` if you are on your extern machine(not the pi)

## installation basic
checkout the script and run
`apt-get install python-setuptools  # for easy_install`
`easy_install pip`
`sudo pip install -r requirements.txt --upgrade`
test with `fab help`

run `fab setup:install` or copy the file ./services/setup/src/config.yml.tpl to ./config.yml
edit the config file for your needs `vim ./config.yml`, do the same with ./services/setup/src/config/*.


then if you want to use the same fab commands locally on the pi `fab pi setup:install` test with `fab pi run:"cd pi-setup && fab help"` prints same like `fab help` but output comes from your pi

install and start all services with `fab pi setup:install_services`


## installation detailed(deb 7)
* burning fresh image to pi's sd card
`fab os:restore`
->sd card number
->file name to store to

* basic config of your raspberry
`ssh pi@[your pi-ip]`
->raspberry
`sudo raspi-config`
->do it

*update/upgrade os and copy pi-service scripts
`fab pi setup:install`

* generate a ssh key if you dont allready have one and add him to your local ssh-agent
`ssh-keygen -t rsa -C "your_email@example.com"`
`ssh-add .ssh/pi_tank_m1_rsa`
`cat .ssh/pi_tank_m1_rsa.pub`
`fab pi os:add_ssh_key`
->paste your copied pi_tank_m1_rsa.pub key
`ssh pi@[your pi-ip]`
->no password needed

* if there re problems ssh connecting without password
`sudo vim /etc/ssh/sshd_config`
->add: AuthorizedKeysFile %h/.ssh/authorized_keys
`sudo service ssh restart`

* install picam service
`fab pi picam:install`
`fab pi picam:start`
->goto [your pi-ip]:8081
`fab pi picam:enable_autostart`

* install piserver service (not yet ready, TODO refactor and move to github)
`fab pi piserver:install`
`fab pi piserver:start`
->goto [your pi-ip]:8000
`fab pi piserver:enable_autostart`

* install webiopi service
`fab pi webiopi:install`
`fab pi webiopi:start`
->goto [your pi-ip]:8083

* backup your fresh new pi os
`fab os:backup`

# Screens
### Desktop
![Desktop](https://github.com/creative-workflow/pi-setup/blob/master/services/setup/screens/desktop.png)
### Backup
![Backup](https://github.com/creative-workflow/pi-setup/blob/master/services/setup/screens/backup.png)
### Mobile
![Mobile](https://github.com/creative-workflow/pi-setup/blob/master/services/setup/screens/mobile.png)

### services
#### backup/restore
connect your pi sd card and
`fab os:backup` -> download a bootable backoup from your pi to ./images
`fab os:restore` -> upload an image from ./images to your pi, see also http://www.raspberrypi.org/downloads/

#### basic
`pi`                          give the target host(your pi) with pi:[your-pi-ip] or pi:[your-pi-ip],[user],[pass]
`help`                        print this help
`run`                         run a command on local or pi `fab run:'ls -al'`
#### os
`os:backup`                   store a bootable image from a sd device to ./images/ (run with sudo)
`os:info`                     get basic information or with pi`*os:info`,extended more detailes
`os:install`
`os:log`                      tail all logs or with pi`*os:log`,/var/log/messages a specific log
`os:restart`                   reboot the pi
`os:restore`                  write a bootable image from ./images/ to sd device
`os:stop`                shout down the pi
`os:uninstall`                removes service files from remote service folder
`os:update`                   run upgrade and clean on the pi
`os:update_firmware`          update the pi firmware
#### picam
`picam:disable_autostart`     disable automatic start of this service
`picam:enable_autostart`      enable automatic start of this service
`picam:install`               setup the `*picam image` service on your pi
`picam:restart`               restart the the service
`picam:start`                 start the the service
`picam:stop`                  stop the the service
`picam:uninstall`             removes service files from remote service folder
`picam:update`                copy service files to remote service folder
#### piserver (TODO refactor and move to github)
`piserver:disable_autostart`  disable automatic start of this service
`piserver:enable_autostart`   enable automatic start of this service
`piserver:install`            checkout and setup simple pi server
`piserver:restart`            restart the the service
`piserver:start`              start the the service
`piserver:stop`               stop the the service
`piserver:uninstall`          removes service files from remote service folder
`piserver:update`             copy service files to remote service folder
`piserver:update_sync`        update git repo, then copy to pi and restart
#### setup
`setup:install`               copy and setup pisetup to your pi, so you can run all commands also locally on your #### pi
`setup:installed`             list installed services
`setup:uninstall`             removes service files from remote service folder
`setup:install_services`      install and start all services
`setup:update`                copy service files to remote service folder
#### webiopi
`webiopi:disable_autostart`   disable automatic start of this service
`webiopi:enable_autostart`    enable automatic start of this service
`webiopi:install`
`webiopi:restart`             restart the the service
`webiopi:start`               start the the service
`webiopi:stop`                stop the the service
`webiopi:uninstall`           removes service files from remote service folder
`webiopi:update`

## contribute
fork this repo and add services, services, services =)

```python
from piservices import PiService
import socket

class PicamService(PiService):
  name             = 'picam'
  init_script      = 'service.sh'
  copy_init_script = True
  apt_get_install  = ['subversion', 'libv4l-dev', 'libjpeg8-dev' ...]

  def install(self):
    """setup the picam image service on your pi"""
    PiService.install(self)
    self.sudo('svn co https://svn.code.sf.net/p/mjpg-streamer/code /etc/mjpg-streamer')
    self.run('cd /etc/mjpg-streamer/mjpg-streamer && sudo make USE_LIB4VL=true clean all && sudo make DESTDIR=/usr install')

  def with_init_script_content_do(self, content):
    return content % {'fps'   : self.config.fps,
                      'led'   : self.config.led,
                      'res'   : self.config.res,
                      'port'  : self.config.port}

instance = PicamService()

```
##TODO
