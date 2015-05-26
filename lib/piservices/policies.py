import sys, os, fabric

class PiServicePolicies:
  @staticmethod
  def is_local():
    return (not fabric.api.env.hosts or fabric.api.env.hosts[0] in ['localhost', '127.0.0.1', '::1'])

  @staticmethod
  def is_pi():
    return os.path.isdir('/home/pi')

  @staticmethod
  def check_local_or_exit():
    if not PiServicePolicies.is_local():
      print "...only callable on localhost!!!"
      sys.exit(-1)

  @staticmethod
  def check_remote_or_exit():
    if PiServicePolicies.is_local():
      print "...only callable on remote host!!!"
      sys.exit(-1)

  def check_installed_or_exit(self):
    if not PiServicePolicies.installed(self):
      print "...first you have to install this service! fab pi %s:install"
      sys.exit(-1)

  def installed(self):
    ret = self.file_exists('__init__.py')
    if not ret: print self.name+' not installed'
    return ret
