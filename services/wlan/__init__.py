import os, csv, re
from piservices import PiService

#http://weworkweplay.com/play/automatically-connect-a-raspberry-pi-to-a-wifi-network/
#sudo vim /etc/network/interfaces ->
# auto wlan0
# allow-hotplug wlan0
# iface wlan0 inet dhcp
# wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
# iface default inet dhcp


class WlanService(PiService):
  name              = "wlan"
  commands          = ['interface']
  config_file       = '/etc/wpa_supplicant/wpa_supplicant.conf'

  def __init__(self):
    PiService.__init__(self)
    self.detector = WlanModuleDetector()

  def deploy(self, restart=True):
    """deploys service module code and system configs"""
    PiService.deploy(self, False)

    content=''
    for network in self.config.networks:
      content+="""
network={
ssid="%(ssid)s"
psk="%(psk)s"
proto=%(proto)s
key_mgmt=%(key_mgmt)s
pairwise=%(pairwise)s
auth_alg=%(auth_alg)s
}

""" % network

    config_writer = self.remote.partial(content, self.config_file)
    config_writer.render()
    config_writer.write()

    if restart:
      self.restart()

  def enable_autostart(self):
    """enable automatic start and try to connect to known networks"""
    loader = self.remote.config.whitespace('/etc/network/interfaces')
    loader.set('auto', 'wlan0') #have to be in the first line
    loader.set('allow-hotplug wlan0')
    loader.set('iface wlan0', 'inet dhcp')
    loader.set('wpa-conf', '/etc/wpa_supplicant/wpa_supplicant.conf')
    loader.unset('wpa-roam')
    loader.set('iface default','inet dhcp')
    loader.write()

    self.sudo('ifup --no-act eth0')
    self.sudo('ifup --no-act wlan0')

    print "now restart you pi with fab pi os:reboot"

  def disable_autostart(self):
    loader = self.remote.config.whitespace('/etc/network/interfaces')
    loader.set('auto', 'lo')
    loader.unset('wpa-conf')
    loader.set('wpa-roam', '/etc/wpa_supplicant/wpa_supplicant.conf')
    loader.write()

  def start(self):
    self.sudo('ifconfig %s up' % self.interface())

  def stop(self):
    self.sudo('ifconfig %s down' % self.interface())

  def restart(self):
    self.start()
    self.stop()

  def interface(self):
    if self.config.interface == 'auto':
      return self.detector.detect_interface()

    return self.config.interface


class WlanModuleDetector:
  csv_file         = os.path.dirname(os.path.realpath(__file__))+'/src/modules.csv'
  module_def       = None

  interface = None
  def detect_interface(self):
    if not self.interface:
      output = instance.run('ip link show | grep -oh "wlan[0-9]*"')
      self.interface = re.findall('(wlan[0-9]*)', output)[0]
    return self.interface

  def lsusb(self):
    return self.service('usb').devices

  def detect_module(self):
    for line in self.lsusb():
      module = self.module_from_match(line)
      if module:
        return module

    return 'module not supported'

  def is_edimax_adapter(self):
    return 'dimax' in '\n'.join(self.lsusb())

  def module_from_match(self, line):
    for rule in self.get_module_def():
      if rule[1].search(line):
        return rule[0]

    return None

  def get_module_def(self):
    if not self.module_def:
      self.module_def = []
      with open(self.csv_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
          row[1] = re.compile(row[1])
          self.module_def.append(row)

    return self.module_def


instance = WlanService()
