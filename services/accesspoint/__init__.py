from piservices import PiService

#http://elinux.org/RPI-Wireless-Hotspot
#http://www.daveconroy.com/using-your-raspberry-pi-as-a-wireless-router-and-web-server/

class AccesspointService(PiService):
  name     = "accesspoint"
  commands = []

  def _walk_used_srvices(self, callback):
    for service_name in self.config.uses_service:
      with self.api.settings(warn_only=True):
        callback(self.service(service_name))

  def _call_used_srvices(self, method, *args, **kwargs):
    def call(service):
      func = getattr(service,method)
      func(*args, **kwargs)

    self._walk_used_srvices(call)


  def install(self):
    PiService.install(self)
    self._call_used_srvices('install')

  def stop(self):
    """shout down the pi"""
    self._call_used_srvices('stop')

  def start(self):
    """shout down the pi"""
    self._call_used_srvices('start')

  def restart(self):
    """reboot the pi"""
    self._call_used_srvices('restart')

  def enable_autostart(self):
    """reboot the pi"""
    self._call_used_srvices('enable_autostart')

  def disable_autostart(self):
    """reboot the pi"""
    self._call_used_srvices('disable_autostart')

  def deploy(self, restart=False):
    """run upgrade and clean on the pi"""
    PiService.deploy(self, False)
    self._call_used_srvices('deploy', False)

    if restart:
      self._call_used_srvices('restart')

  def info(self, extended=False):
    """get basic information """
    print "used services:"
    print self.config.uses_service


    #sudo vim /etc/ssh/sshd_config
    #add: AuthorizedKeysFile      %h/.ssh/authorized_keys
    #sudo service ssh restart
    #self.sudo('service ssh restart')

instance = AccesspointService()
