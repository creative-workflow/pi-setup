from piservices import PiService
import re

class LanService(PiService):
  name            = "lan"
  managed_service = False
  commands        = ['start', 'stop', 'restart', 'interface']

  def stop(self):
    """shout down the pi"""

  def restart(self):
    """reboot the pi"""

  def info(self, extended=False):
    """get basic information"""
    print "interface: %s" % self.interface()

  def interface(self):
    if self.config.interface == 'auto':
      return self._autodetect_interface()

    return self.config.interface

  def _autodetect_interface(self):
    output = self.run('ip link show | grep -oh "lan[0-9]*"')
    return re.findall('(lan[0-9]*)', output)[0]


instance = LanService()
