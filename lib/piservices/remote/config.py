import re
from base import AbstractRemoteLoader
from configobj import ConfigObj
from StringIO import StringIO
from ConfigParser import ConfigParser

class AbstractRemoteConfigLoader(AbstractRemoteLoader):
  def __init__(self, service, remote_file = None):
    AbstractRemoteLoader.__init__(self, service, remote_file)
    self.cfg = None

  def create_config_object(self, fd):
    raise Exception('not implemented')

  def load(self, remote_file = None):
    AbstractRemoteLoader.load(self, remote_file)
    self.cfg = self.create_config_object()
    return self.cfg

  def prepare_content_for_write(self):
    fd = StringIO()
    self.cfg.write(fd)
    fd.seek(0)
    self.content = fd.read()

  def set(self, key, value):
    if not self.cfg: self.load()
    self.cfg[key] = value
    return self

  def unset(self, key):
    if not self.cfg: self.load()
    del self.cfg[key]
    return self

  def get(self, key):
    if not self.cfg: self.load()
    return self.cfg[key]

  def all(self):
    if not self.cfg: self.load()
    return self.cfg

class RemoteConfigIniLoader(AbstractRemoteConfigLoader):
  def create_config_object(self):
    return ConfigObj(self.fd, indent_type='')

class RemoteShellVarsLoader(RemoteConfigIniLoader):
  def __init__(self, service, remote_file = None, quotes='"'):
    RemoteConfigIniLoader.__init__(self, service, remote_file)
    self.quotes = quotes

  #we have to re add the quotes
  def prepare_content_for_write(self):
    RemoteConfigIniLoader.prepare_content_for_write(self)
    result = []
    for line in self.content.split('\n'):
      if ' = ' in line:
        line = line.replace(' = ', '='+self.quotes)+self.quotes
      result.append(line)

    self.content = '\n'.join(result)


class RemoteConfigParser(AbstractRemoteConfigLoader):
  def create_config_object(self, fd):
    cfg = ConfigParser()
    cfg.readfp(fd)
    return cfg

  def set(self, section, key, value):
    if not self.cfg: self.load()
    self.cfg.set(section, key, value)
    return self

  def unset(self, section, key):
    if not self.cfg: self.load()
    self.cfg.remove_option(section, key)
    return self

  def get(self, section, key):
    if not self.cfg: self.load()
    return self.cfg.get(section, key)

  def all(self):
    if not self.cfg: self.load()
    return self.cfg.items()

class RemoteWhitespaceConfigLoader(RemoteConfigIniLoader):
  def create_config_object(self):
    return WhitespaceConfigEditor(self.fd)

  def set(self, key, value=''):
    if not self.cfg: self.load()
    self.cfg.set(key, value)
    return self

  def unset(self, key):
    if not self.cfg: self.load()
    self.cfg.unset(key)
    return self

  def get(self, key):
    if not self.cfg: self.load()
    return self.cfg.get(key)

  def all(self):
    if not self.cfg: self.load()
    return self.cfg.all()


class WhitespaceConfigEditor:
  def __init__(self, fd, comment='#'):
    fd.seek(0)
    self.content = fd.read()
    self.content = re.sub('[ \t]+', ' ', self.content)
    self.comment = comment

  def write(self, fd):
    fd.seek(0)
    fd.write(self.content)

  def set(self, key, value='', pos=None):
    if not key in self.content:
      self.content+= ('\n'+key+' '+value)
    else:
      lines = self.content.splitlines()
      nr = -1
      for line in lines:
        nr+=1
        if key in line:#process all line, maybe key is present multiple times or in comments
          lines[nr] = self._process_line(line, key, value)

      self.content = '\n'.join(lines)

  def _process_line(self, line, key, value):
    if not self.comment in line:
      return key+' '+value

    tmp  = line.split(self.comment)

    return key+' '+value+' '+self.comment+' '+tmp[1]

  def unset(self, key):
    lines = self.content.splitlines()
    nr = -1
    for line in lines:
      nr+=1
      if key in line:#process all line, maybe key is present multiple times or in comments
        if self.comment in line:
          tmp = line.split(self.comment)
          if not key in tmp[0]:
            continue

        del lines[nr]

    self.content = '\n'.join(lines)

  def get(self, key):
    if not key in self.content:
      return None

    lines = self.content.splitlines()
    nr = -1
    for line in lines:
      nr+=1
      if key in line:#process all line, maybe key is present multiple times or in comments
        if not self.comment in line:
          return line.split(' ').pop()

        tmp = line.split(self.comment)
        if not key in tmp[0]:
          continue

        return tmp[0].split(' ').pop()

    return None

  def all(self):
    return self.content.splitlines()
