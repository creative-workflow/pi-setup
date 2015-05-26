from piservices import PiService

class WebIoPiService(PiService):
  name               = 'webiopi'
  web_io_config_file = '/etc/webiopi/config'
  init_script        = '/etc/init.d/webiopi'

  def install(self):
    PiService.install(self)
    self.sudo('chmod +x src/{play.sh,setup.sh}')
    self.run(' cd src && sudo ./setup.sh')
    self.update()

  def deploy(self, restart=True):
    try:
      loader = self.config.remote.parser(self.web_io_config_file)
      loader.load()
      loader.set('HTTP', 'port', self.config.port)
      loader.write()
    except:
      print "...when webiopi is not installed, we cannot modify the file "+self.web_io_config_file

    PiService.deploy(self, restart)

instance = WebIoPiService()
