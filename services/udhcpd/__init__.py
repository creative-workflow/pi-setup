from piservices import PiService

class UdhcpdService(PiService):
  name            = "udhcpd"
  apt_get_install = [ 'udhcpd' ]
  config_file     = '/etc/default/udhcpd'
  service_file    = '/etc/udhcpd.conf'
  commands        = ['enable', 'disable']

  def start(self):
    """start the service"""
    self.enable()
    self.sudo("sudo ifconfig %s %s" % (self._interface(), self.config.opt.router))
    self.sudo('service udhcpd start')

  def stop(self):
    """stop the service"""
    self.sudo('service udhcpd stop')

  def restart(self):
    """restart the service"""
    self.sudo("sudo ifconfig %s %s" % (self._interface(), self.config.opt.router))
    self.sudo('service udhcpd restart')

  def deploy(self, restart=False):
    """run upgrade and clean on the pi"""
    PiService.deploy(self, False)

    self._udhcpd_default_write(self.config.enabled)

    config_loader = self.remote.config.whitespace(self.service_file)
    for key, value in self.config.iteritems():
      if key == 'enabled': continue
      if key == 'opt':
        for sub_key, sub_value in value.iteritems():
          config_loader.set('opt '+sub_key, sub_value)
      else:
        config_loader.set(key, value)

    config_loader.set('interface', self._interface())
    config_loader.write()

    # TODO /interfaces
    # iface wlan0 inet static
    # address 192.168.42.1
    # netmask 255.255.255.0
    # #allow-hotplug wlan0
    # #wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
    # #iface default inet dhcp

    if restart:
      self.restart();

  def enable(self):
    self._udhcpd_default_write('yes')

  def disable(self):
    self._udhcpd_default_write('no')

  def enable_autostart(self):
    """enable automatic start of this service"""
    self.enable()
    PiService.enable_autostart(self)

  def _interface(self):
    if self.config.interface == 'auto':
      return self.service('wlan').interface()

    return self.config.interface

  def _udhcpd_default_write(self, value):
    config_loader = self.remote.config.shellvars(self.config_file)
    config_loader.load()
    config_loader.set('DHCPD_ENABLED', value)
    config_loader.write()

instance = UdhcpdService()
