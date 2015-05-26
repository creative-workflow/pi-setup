from piservices import PiService

#with edimax wlan
#http://jenssegers.be/blog/43/realtek-rtl8188-based-access-point-on-raspberry-pi

#with
#  Panda Ultra, Mid-Range and 300Mbps Wireless N adapters support Access Point
#  Ralink RT5370 and RT5372 DO support Access Point
#  irLink 101 / AWL5088 does NOT support Access Point

class HostapdService(PiService):
  name            = "hostapd"
  apt_get_install = [ 'hostapd' ]
  init_script     = '/etc/init.d/hostapd'
  config_file     = '/etc/hostapd/hostapd.conf'
  service_file    = '/etc/default/hostapd'

  def info(self, extended=False):
    """show remote config"""
    self.sudo('cat %s' % self.config_file)

  def install(self):
    PiService.install(self)

    if self._is_edimax_adapter():#install fixed edimax hostapd binary
      self.sudo('unzip src/hostapd.zip')
      self.sudo('mv /usr/sbin/hostapd /usr/sbin/hostapd.bak || true')
      self.sudo('mv hostapd /usr/sbin/hostapd.edimax')
      self.sudo('ln -sf /usr/sbin/hostapd.edimax /usr/sbin/hostapd')
      self.sudo('chown root.root /usr/sbin/hostapd')
      self.sudo('chmod 755 /usr/sbin/hostapd')

  def deploy(self, restart=True):
    """update pi service config"""
    PiService.deploy(self, False)

    #write etc/hostapd/hostapd.conf
    loader = self.remote.config.shellvars(self.config_file, quotes='')
    for key, value in self.config.iteritems():
      loader.set(key, value)

    loader.set('driver', self._driver())
    loader.set('interface', self._interface())
    loader.write()

    #write /etc/default/hostapd
    loader = self.remote.config.shellvars(self.service_file)
    loader.set('DAEMON_CONF', self.config_file)
    loader.write()

    if restart:
      self.restart()

  def start(self):
    """start the service"""
    self.sudo('service hostapd start')

  def stop(self):
    """stop the service"""
    self.sudo('service hostapd stop')

  def restart(self):
    """restart the service"""
    self.sudo('service hostapd restart')

  def _is_edimax_adapter(self):
    for device in self.service('usb').devices(do_print=False):
      if 'dimax' in device:
        return True

    return False

  def _driver(self):
    if self._is_edimax_adapter():
      return 'rtl871xdrv'

    else:
      return self.config.driver

  def _interface(self):
    if self.config.interface == 'auto':
      return self.service('wlan').interface()

    return self.config.interface

instance = HostapdService()
