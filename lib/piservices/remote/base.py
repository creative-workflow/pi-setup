from StringIO import StringIO
import color

class AbstractRemoteLoader:
  def __init__(self, service, remote_file = None):
    self.service     = service
    self.remote_file = remote_file
    self.content     = ''
    self.fd          = None

  def load(self, remote_file = None):
    if remote_file:
      self.remote_file = remote_file

    try:
      with self.service.api.hide('output','running'):
        self.service.run('sudo mkdir -p $(dirname %(f)s) && sudo touch %(f)s' % {'f': self.remote_file})
        self.content = self.service.run('sudo cat %s' % self.remote_file)
    except:
      pass #no problem ...file doesnt exist, we will create

    self.fd = StringIO(self.content)
    self.fd.seek(0)

  def prepare_content_for_write(self):
    pass

  def write(self, remote_file=None, content=None, resulting_user='root', resulting_group='root'):
    if not remote_file:
      remote_file = self.remote_file

    if not remote_file:
      remote_file = ''

    if content:
      self.content = content

    self.backup_if_no_backup_exists(remote_file)

    self.prepare_content_for_write()

    with color.for_put():
      print "\n>> writing config: "+remote_file+"\n"+('='*30)+"\n"+self.content+"\n\n"

    fd = StringIO(self.content)
    fd.seek(0)
    fd.write(self.content+'\n')
    fd.seek(0)
    self.service.run('sudo mkdir -p $(dirname %(f)s) && sudo touch %(f)s && sudo truncate -s 0 %(f)s' % {'f': remote_file})
    self.service.put(fd, remote_file, use_sudo=True)
    self.service.sudo('chown %s:%s %s' % (resulting_user, resulting_group, remote_file))

  def backup_if_no_backup_exists(self, remote_file):
    i = remote_file
    o = '%s.pisetup.bak' % i
    if self.service.file_exists(i) and not self.service.file_exists(o):
      self.service.cp(i, o)
