from piservices import PiService
import socket

class PicamService(PiService):
  name             = "picam"
  apt_get_install  = ['build-essential', 'subversion', 'libv4l-dev', 'libjpeg8-dev', 'imagemagick']
  commands         = ['paths', 'endpoint']
  init_script      = 'service.sh'

  def install(self):
    """setup the picam image service on your pi"""
    PiService.install(self)
    self.sudo('svn co https://svn.code.sf.net/p/mjpg-streamer/code /etc/mjpg-streamer')
    self.run('cd /etc/mjpg-streamer/mjpg-streamer && sudo make USE_LIB4VL=true clean all && sudo make DESTDIR=/usr install')

  def with_init_script_content_do(self, content):
    return content % {'fps'   : self.config.fps,
                      'led'   : self.config.led,
                      'res'   : self.config.res,
                      'port'  : self.config.port}

  def paths(self):
    endpoint = self.endpoint()
    return {
      'web': endpoint,
      'stream': endpoint+'/?action=stream',
      'static': endpoint+'/?action=snapshot'
    }

  def endpoint(self):
    return socket.gethostname()+':'+self.config.port

instance = PicamService()

#--yuv ] enable YUYV format and disable MJPEG mode
#[-q | --quality
