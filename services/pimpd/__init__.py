from piservices import PiService

class MusicPlayerDaemonService(PiService):
  name            = 'pimpd'
  apt_get_install = [ 'mpd', 'mpc', 'alsa-utils']
  path_to_music   = '/var/lib/mpd/music'
  init_script     = 'installed'
  config_file     = '/etc/mpd.conf'
  config_file_tpl = 'src/mpd.conf'


  #TODO mpd conf

  def install(self):
    PiService.install(self)

    self.sudo('modprobe snd_bcm2835')
    self.sudo('amixer cset numid=3 1')
    self.sudo('chmod g+w /var/lib/mpd/music/ /var/lib/mpd/playlists/')
    self.sudo('chgrp audio /var/lib/mpd/music/ /var/lib/mpd/playlists/')

  def deploy(self, restart=True):
    config_writer = self.remote.template(self.config_file_tpl)
    config_writer.render({
                         'host': self.config.host,
                         'port':self.config.port
                         })

    config_writer.write(self.config_file)

    PiService.deploy(self, restart)

    self.sudo('mpc update')

  def start(self):
    self.sudo('/etc/init.d/mpd start')
    self.sudo('mpc update')

  def restart(self):
    self.sudo('/etc/init.d/mpd restart')
    self.sudo('mpc update')

  def stop(self):
    self.sudo('/etc/init.d/mpd stop')

instance = MusicPlayerDaemonService()
