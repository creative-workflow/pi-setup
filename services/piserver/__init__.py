import os
from piservices import PiService

class PiServerService(PiService):
  name             = 'piserver'
  init_script      = 'src/service.sh'
  copy_init_script = True
  commands         = ['deploy_pull_master']
  apt_get_install  = ['python-rpi.gpio', 'libavformat-dev', 'libav-tools',
                      'libopencv-dev', 'v4l-utils', 'ffmpeg', 'python-imaging', 'libc6-dev',
                      'python-opencv','git-core', 'git']

  git_repo = 'git@5.45.97.194:pi-tank/pi-server.git'

  def install(self):
    """checkout and setup simple pi server"""

    self.clean_git_checkout(self.git_repo, '/src')

    self.__copy_config_templates();

    self.local("sudo pip install -r src/requirements.txt --upgrade")

    if not self.is_local():
      PiService.install(self)  #copy to remote

      self.sudo("pip install -r src/requirements.txt --upgrade")

  def __copy_config_templates(self):
    config_tpl_folder = self.local_path+"/src/config/tpl"
    if(os.path.isdir(config_tpl_folder)):
      print 'dont copy config templates, because you have allready some, check if there wehere changes in '+config_tpl_folder
    else:
      self.ops.local("cp -n "+config_tpl_folder+"* "+self.local_path+"/src/config/")


  def deploy_pull_master(self, restart=True):
    """update git repo, then copy to pi and restart"""
    self.ops.local("cd "+self.local_path+"/src && git reset --hard HEAD && git pull origin master && git submodule update")
    PiService.deploy(self, restart)

instance = PiServerService()
