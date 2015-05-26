
class DictAsObject(dict):
  def __getattr__(self, name):
    return self.__getitem__(name)

  def __getitem__(self, name):
    value = dict.__getitem__(self, name)
    if isinstance(value, dict) and not isinstance(value, DictAsObject):
      value = DictAsObject(value)
      dict.__setitem__(self, name, value)
    return value

  def __setattr__(self, name, value):
    if isinstance(value, dict) and not isinstance(value, DictAsObject):
      value = DictAsObject(value)
    dict.__setitem__(self, name, value)

  def __delattr__(self, name):
    return self.__delitem__(name)
