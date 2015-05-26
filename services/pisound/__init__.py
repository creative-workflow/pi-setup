from piservices import PiService
from pprint import pprint

#http://pythonhosted.org/python-mpd2/topics/getting-started.html

class SoundService(PiService):
  name            = "pisound"
  apt_get_install = ['git-core', 'git', 'cmake', 'libmpdclient-dev' ]
  init_script     = 'auto'
  commands        = ['play', 'pause', 'volume', 'laughing', 'radio', 'morse', 'pic', 'hiphop']
  git_repo        = 'https://github.com/notandy/ympd'

  def install(self):
    mpd = self.service('pimpd')
    if not mpd.installed():
      mpd.install()

    self.clean_git_checkout(self.git_repo, 'src/web')

    PiService.install(self)

    self.run('cp -R ./src/fx %s/fx' % mpd.path_to_music)
    self.sudo('chmod g+w %s/fx'     % mpd.path_to_music)
    self.sudo('chgrp audio %s/fx'   % mpd.path_to_music)

    self.sudo('pip install python-mpd2')
    self.api.local('pip install python-mpd2')

    self.run('cd src/web && mkdir -p build && cd build && cmake ..  -DCMAKE_INSTALL_PREFIX:PATH=/usr && make && sudo make install')

  def with_init_script_content_do(self, content):
    return content % {'name'   : self.name,
                      'daemon' : self.remote_path+'/src/web/build/ympd',
                      'command': '-h %s -p %s -w %s' % (self.config.host, self.config.port, self.config.web ),
                      'path'   : self.remote_path}

  def deploy(self, restart=True):
    self.service('pimpd').deploy(restart)
    PiService.deploy(self, restart)

  def start(self):
    self.service('pimpd').start()
    PiService.start(self)

  def stop(self):
    PiService.stop(self)

  def restart(self):
    PiService.restart(self)

  def enable_autostart(self):
    """enable automatic start of this service"""
    self.service('pimpd').enable_autostart()
    PiService.enable_autostart(self)

  def disable_autostart(self):
    """disable automatic start of this service"""
    self.service('pimpd').disable_autostart()
    PiService.disable_autostart(self)

  def play(self, path):
    sid = self._client().addid(path)
    self._client().playid(sid)

  def pause(self, path='farts/fart1.mp3'):
    self._client().pause()

  def volume(self,val=80):
    self._client().setvol(val)

  def info(self):
    print "mpd version", self._client().mpd_version
    print self._client().status()
    pprint(self._client().listall(''))

  def laughing(self):
    self.play('fx/laughing.wav')

  def radio(self):
    self.play('fx/radio.wav')

  def morse(self):
    self.play('fx/morse.wav')

  def pic(self):
    self.play('fx/pic.wav')

  def hiphop(self):
    self.play('fx/hiphop.mp3')

  client = None
  def _client(self):
    from mpd import MPDClient
    if not self.client:
      host = self.config.host
      if not self.is_local():
        host = self.api.env.host

      self.client             = MPDClient()
      self.client.timeout     = self.config.timeout
      self.client.idletimeout = self.config.idletimeout
      self.client.connect(host, self.config.port)

    return self.client

instance = SoundService()
