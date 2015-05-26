from piservices import PiService
import piservices

class NatService(PiService):
  name         = "nat"
  sys_ctl_file = '/etc/sysctl.conf'
  init_script  = True
  commands     = ['enable', 'disable']

  def start(self):
    self.sudo('sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"')

  def stop(self):
    """shout down the pi"""
    self.sudo('sh -c "echo 0 > /proc/sys/net/ipv4/ip_forward"')

  def deploy(self, restart=True):
    """run upgrade and clean on the pi"""
    PiService.deploy(self, False)

    if self.config.enabled:
      self.enable()
    else:
      self.disable()

    for i, o in self.config.mappings:
      if i == 'auto': i = self.service('lan').interface()
      if o == 'auto': o = self.service('wlan').interface()
      self._do_mapping(i, o)

    if restart:
      self.restart();

  def enable(self):
    for i, o in self.config.mappings:
      self._do_mapping(i, o)

    self.sudo('sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"')

  def disable(self):
    self.sudo('sh -c "echo 0 > /proc/sys/net/ipv4/ip_forward"')

  def enable_autostart(self):
    """enable automatic start of this service"""
    self.deploy(restart=False);

    self._sysctl_write('1')

    self.sudo('sh -c "iptables-save > /etc/iptables.ipv4.nat"')

    #Now edit the file /etc/network/interfaces and add the following line to the bottom of the file:
    #up iptables-restore < /etc/iptables.ipv4.nat

  def disable_autostart(self):
    """disable automatic start of this service"""
    self._sysctl_write('0')

    #Now edit the file /etc/network/interfaces and remove the following line to the bottom of the file:
    #up iptables-restore < /etc/iptables.ipv4.nat

  def _sysctl_write(self, value):
    loader = self.remote.config.shellvars(self.sys_ctl_file, quotes='')
    loader.set('net.ipv4.ip_forward', value)
    loader.write()

  def _do_mapping(self, i, o):
    self.sudo('iptables -t nat -A POSTROUTING -o %s -j MASQUERADE' % o)
    self.sudo('iptables -A FORWARD -i %s -o %s -m state --state RELATED,ESTABLISHED -j ACCEPT' % (o, i))
    self.sudo('iptables -A FORWARD -i %s -o %s -j ACCEPT' % (i, o))


instance = NatService()
