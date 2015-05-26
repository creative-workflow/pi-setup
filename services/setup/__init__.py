from piservices import PiService
import piservices, os

#TODO
#implement raspi-config replacement via config file and shell commands
#see http://www.sbprojects.com/projects/raspberrypi/tweaks.php

class SetupService(PiService):
  local_path      = os.path.realpath(os.path.dirname(__file__))+'/../../'
  remote_path     = piservices.pisetup_root_folder_on_pi
  name            = 'setup'
  source_files    = ['lib', 'requirements.txt', 'fabfile.py', 'test*', 'config*', 'services/setup/*']
  apt_get_install = ['python-dev', 'python-pip', 'python-unittest2']
  managed_service = False
  commands        = ['installed', 'install_services']

  def install(self):
    """copy and setup pisetup to your pi, so you can run all commands also locally on your pi, also do a system update and upgrade"""
    self.service('os').install()
    self.service('usb').install()

    self.__local_setup()

    if not self.is_local():
      PiService.install(self)
      self.__remote_setup()

  def installed(self):
    """list installed services"""
    self.run('ls services/')

  def install_services(self, *args):
    """install and start all services"""
    if not args or not len(args):
      args = piservices.list_services()

    for service in args:
      if not service in ['os', 'setup', 'usb']:
        self.service(service).install()

    for service in args:
      if not service in ['os', 'setup', 'usb']:
        self.service(service).start()

  def __local_setup(self):
    self.ops.local("mkdir -p ./images")
    self.ops.local("test ! -f ./config.yml && cp ./services/pisetup/src/config.yml.tpl ./config.yml || true")
    self.ops.local("test ! -d ./config && cp -R ./services/pisetup/src/config/* ./config/ || true")

  def __remote_setup(self):
    self.sudo('pip install --upgrade pip')
    self.sudo('pip install -r requirements.txt --upgrade')
    self.run('cd %s && fab' % self.remote_pi_setup_path)


instance = SetupService()
