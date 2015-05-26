from config import *
from template import *
from dictasobject import DictAsObject

class RemoteFileHelper:
  def __init__(self, service):
    self.service = service
    self.config = DictAsObject({
      'ini'        : self.config_ini,
      'parser'     : self.config_parser,
      'shellvars'  : self.config_shellvars,
      'whitespace' : self.config_whitespace
    })

  def build_local_lpath(self, path):
    if not path:
      return path

    if path and path.startswith('/'):
      return path

    if os.path.isfile(self.service.local_path+'/'+path):
      return self.service.local_path+'/'+path

    return path

  def abstract(self, remote_file=None):
    return AbstractRemoteLoader(self.service,
                                self.build_remote_path(remote_file))

  def template(self, local_path, remote_path=None, *args, **kwargs):
    return RemoteConfigFileWithTemplate(self.service,
                                        self.build_local_lpath(local_path),
                                        remote_path,
                                        *args, **kwargs)

  def partial(self, local_path, remote_path=None, *args, **kwargs):
    return RemoteConfigFileWithPartial( self.service,
                                        self.build_local_lpath(local_path),
                                        remote_path, *args, **kwargs)

  def config_ini(self, remote_file = None, *args, **kwargs):
    if remote_file: remote_file = self.service.normalize_path(remote_file)
    return RemoteConfigIniLoader(self.service, remote_file, *args, **kwargs)

  def config_parser(self, remote_file = None, *args, **kwargs):
    if remote_file: remote_file = self.service.normalize_path(remote_file)
    return RemoteConfigParser(self.service, remote_file, *args, **kwargs)

  def config_shellvars(self, remote_file = None, *args, **kwargs):
    if remote_file: remote_file = self.service.normalize_path(remote_file)
    return RemoteShellVarsLoader(self.service, remote_file, *args, **kwargs)

  def config_whitespace(self, remote_file = None, *args, **kwargs):
    if remote_file: remote_file = self.service.normalize_path(remote_file)
    return RemoteWhitespaceConfigLoader(self.service, remote_file, *args, **kwargs)
