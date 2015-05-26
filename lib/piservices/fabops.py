import os, color
from fabric import operations, api
from fabric.contrib import files
from policies import PiServicePolicies


class FabricTaskOperator:
  def __init__(self, local_path, remote_path):
    self.remote_path = remote_path
    self.local_path  = local_path
    self.ops = operations
    self.api = api
    self.env = api.env

  def run(self, command, *args, **kwargs):
    try:
      with color.for_run():
        if self.is_local():
          return self.ops.local('cd %s && %s' % (self.local_path, command), *args, **kwargs)
        else:
          return self.ops.run('cd %s && %s' % (self.remote_path, command), *args, combine_stderr=True, pty=False, **kwargs)
    except Exception as e:
      with color.for_error():
        raise e


  def local(self, command, *args, **kwargs):
    try:
      with color.for_run():
        return self.ops.local('cd %s && %s' % (self.local_path, command), *args, **kwargs)
    except Exception as e:
      with color.for_error():
        raise e

  def sudo(self, command, *args, **kwargs):
    return self.run('sudo %s' % command, *args, **kwargs)

  def put(self, src, dest='', *args, **kwargs):
    with color.for_put():
      with self.api.settings(warn_only=True):
        self.ops.put(src, self.normalize_path(dest), *args, **kwargs)

  def get(self, src, dest='', *args, **kwargs):
    with color.for_get():
      with self.api.settings(warn_only=True):
        self.ops.get(self.normalize_path(src), dest, *args, **kwargs)

  def cd(self, path="~/"):
    return self.run(path)

  def file_exists(self, path):
    if not path: return False
    method = files.exists
    if PiServicePolicies.is_local():
      method = os.path.isfile

    return method(self.normalize_path(path))

  def cp(self, i, o):
    self.sudo('cp %s %s' % (self.normalize_path(i), self.normalize_path(o)))

  def normalize_path(self, path):
    if path.startswith('/'): return path
    return self.remote_path+'/'+path

  def zip_files_and_copy(self, file_list, target):
    if not file_list or len(file_list) < 1: return

    #make path relative, so they will be extracted correct on the remote end
    file_list = [x.replace(self.local_path+'/', '') for x in file_list]

    tmp_file_list = '/tmp/pisetup.%s.transfer.list' % self.name
    tmp_archive   = '/tmp/pisetup.%s.transfer.tar' % self.name
    with open(tmp_file_list, 'w') as f:
      f.write('\n'.join(file_list))

    self.api.local('cd %s && tar cvf - -T %s > %s' % (self.local_path, f.name, tmp_archive))
    self.put(tmp_archive, '/tmp/', use_sudo=True)
    self.run('tar xvf %s -C %s ' % (tmp_archive, target))

    os.unlink(f.name)
    os.unlink(tmp_archive)

  def clean_git_checkout(self, git_repo, target):
    target = self.local_path+'/'+target
    if os.path.isdir(target+'/.git'):
      self.ops.local('cd %s && git checkout master' % target)
      self.ops.local('cd %s && git reset --hard origin/master' % target)
    else:
      self.ops.local('mkdir -p '+target)
      self.ops.local('cd '+target+" && git clone "+git_repo+" . && git submodule init && git submodule update")

