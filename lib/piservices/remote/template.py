from base import AbstractRemoteLoader
import os

class RemoteConfigFileWithTemplate(AbstractRemoteLoader):
  def __init__(self, service, template_file = None, remote_file = None):
    AbstractRemoteLoader.__init__(self, service, remote_file)
    self.template_file = template_file
    self.template      = ''

  def render(self, replacements={}):
    if not self.template:
      self.load_template()

    self.content = self.template % replacements

  def replace(self, replacements):
    if not self.template:
      self.load_template()

    self.content = self.template
    for key, value in replacements.iteritems():
      self.content = self.content.replace(key, str(value))

  def load_template(self):
    if os.path.isfile(self.template_file):
      with open(self.template_file) as fd:
        self.template = fd.read()

    elif self.template_file:
      self.template = self.template_file

    return self.template


class RemoteConfigFileWithPartial(RemoteConfigFileWithTemplate):
  def __init__(self, service, template_file = None, remote_file = None, separator = '# RemoteConfigFileWithPartial-Divder ...DO NOT CHANGE!!!'):
    RemoteConfigFileWithTemplate.__init__(self, service, template_file, remote_file)
    self.separator = separator

  def clean(self):
    tmp = self.content.split(self.separator)
    if len(tmp) > 1:
      tmp.pop(1)              #remove old appendings

    self.content = '\n'.join(tmp)

    return self.content

  def render(self, replacements={}):
    if not self.content:
      self.load()

    self.clean()

    if not self.template:
      self.load_template()

    self.template = self.content+'\n\n'+self.separator+'\n'+self.template+'\n'+self.separator

    self.template = self.template.replace('\n\n', '\n')

    return RemoteConfigFileWithTemplate.render(self, replacements)
