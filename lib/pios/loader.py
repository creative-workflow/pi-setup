import sys, os, osx, linux

def is_linux():
  return (sys.platform == 'linux' or sys.platform == 'linux2')

def is_osx():
  return sys.platform == 'darwin'

def is_windows():
  return sys.platform == 'win32'


def get_wrapper(wrapper = None):
  if not wrapper:
    if is_linux():
      return linux.wrapper

    if is_osx():
      return osx.wrapper

    raise Exception('os %s not supported' % os.name)
