from piservices import PiService

class UsbService(PiService):
  name            = "usb"
  managed_service = False
  commands        = ['devices']

  def info(self):
    """get basic information"""
    self.devices()
    self.sudo('lsusb && lsusb -tv')

  lsusb_result = None
  def devices(self, do_print = True):
    if not self.lsusb_result:
      self.lsusb_result = self.run('lsusb').splitlines()

    if do_print:
      print self.lsusb_result

    return self.lsusb_result


instance = UsbService()
