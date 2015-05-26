import yaml, os
from dictasobject import DictAsObject

config_file   = os.path.dirname(os.path.realpath(__file__))+'/../config.yml'

loaded_files = []
config_dict  = {}
def from_file(file_name, defaults={}):
  global loaded_files, config_dict
  config_dict = defaults

  with open(file_name, 'r') as f:
    config_dict = DictAsObject(yaml.load(f))

  if config_dict.has_key('services'):
    for key, value in config_dict.services.iteritems():
      if 'file:' in value:
        file_name = value.split(':').pop()
        file_path = os.path.dirname(os.path.abspath(__file__))+'/../'+file_name
        with open(file_path, 'r') as f:
          config_dict.services[key] = DictAsObject(yaml.load(f))

  return config_dict

def get(key=None):
  global config_dict
  if not key: return config_dict
  return config_dict[key]


#loading the project config with default values
from_file(config_file, {'fabric': {
                            'hosts': ['localhost']},
                            'services':{'path': './services'},
                            'stages': {'default':{}
                          }
                       })


