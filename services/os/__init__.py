from piservices import PiService
import pios.recovery

class OsService(PiService):
  name            = "os"
  apt_get_install = [ 'unzip', 'zip', 'curl', 'ntp', 'ntpdate', 'git-core', 'git', 'wget',
                      'ca-certificates', 'binutils', 'raspi-config', 'mc', 'vim', 'vim-nox',
                      'htop']

  managed_service = False
  commands        = ['stop', 'reboot', 'update_firmware', 'log', 'backup', 'restore', 'add_ssh_key']

  def install(self):
    #PiService.install(self)
    if not self.is_local():
        self.deploy()
        self.sudo('update-alternatives --install /usr/bin/python python /usr/bin/python2.7 10')

  def stop(self):
    """shout down the pi"""
    self.sudo('shutdown -h now')

  def reboot(self):
    """rboot system"""
    self.sudo('reboot')

  def deploy(self, restart=False):
    """run upgrade and clean on the pi"""
    PiService.deploy(self, restart=False)
    self.run('export TERM=linux && sudo apt-get -y update')
    self.run('export TERM=linux && sudo apt-get -y dist-upgrade')
    self.sudo('apt-get -y autoremove')
    self.sudo('apt-get -y autoclean')

  def update_firmware(self):
    """update the pi firmware"""
    #download firmware update script
    self.sudo('wget http://goo.gl/1BOfJ -O /usr/bin/rpi-update && chmod +x /usr/bin/rpi-update')
    #(server usage: 240MB RAM / 16MB Video)
    self.sudo('rpi-update 240') #rpi-update 224 for desktop
    self.sudo('shutdown -r now')

  def info(self, extended=False):
    """get basic information or with pios:info,extended more detailes"""
    if not extended:
      self.sudo('uname -a && uptime')
      self.sudo('ifconfig -a | grep inet')
      self.sudo('lsusb')
      self.sudo('df -hT')
      return

    self.sudo('uname -a && uptime')
    self.run('echo "\nmem, cpu, dev \n============="')
    self.sudo('cat /proc/{meminfo,cpuinfo,devices} ')
    self.run('echo "\nfstab, disk free \n============="')
    self.sudo('cat /etc/fstab && df -hT')
    self.run('echo "\nusb \n============="')
    self.sudo('lsusb && lsusb -tv')
    self.run('echo "\nifconfig \n============="')
    self.sudo('ifconfig -a')

  def log(self, path='/var/log/*'):
    """tail all logs or with pios:log,/var/log/messages a specific log"""
    self.sudo('tail -f %s' % path)

  def backup(self, sd=None, file_name=None):
    """store a bootable image from a sd device to ./images/ (run with sudo)"""
    self.check_local_or_exit()
    pios.recovery.backup(sd, file_name)

  def restore(self, sd=None, file_name=None):
    """write a bootable image from ./images/ to sd device"""
    self.check_local_or_exit()
    pios.recovery.restore(sd, file_name)

  def add_ssh_key(self):
    key = self.ops.prompt("give public key content:")

    self.sudo('mkdir -p /home/pi/.ssh')
    self.sudo('touch /home/pi/.ssh/authorized_keys')
    self.sudo('echo "%s" | sudo tee -a /home/pi/.ssh/authorized_keys' % key)

    #sudo vim /etc/ssh/sshd_config
    #add: AuthorizedKeysFile      %h/.ssh/authorized_keys
    #sudo service ssh restart
    self.sudo('service ssh restart')


instance = OsService()
