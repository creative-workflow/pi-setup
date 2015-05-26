from tests import Case

from dictasobject import DictAsObject

class TestDictAsObject(Case):
  def test_set_dict(self):
    dao = DictAsObject()
    dao['key']='value'

    assert dao['key'] == 'value'

  def test_remove_dict(self):
    dao = DictAsObject()
    dao['key']='value'

    assert len(dao) is 1
    del dao['key']
    assert len(dao) is 0

  def test_set_object(self):
    dao = DictAsObject()
    dao.key='value'

    assert dao.key == 'value'

  def test_remove_object(self):
    dao = DictAsObject()
    dao.key='value'

    assert len(dao) is 1
    del dao.key
    assert len(dao) is 0

  def test_set_object_read_dict(self):
    dao = DictAsObject()
    dao.key='value'

    assert dao['key'] == 'value'

  def test_set_dict_read_object(self):
    dao = DictAsObject()
    dao['key']='value'

    assert dao.key == 'value'

  def test_set_object_remove_dict(self):
    dao = DictAsObject()
    dao.key='value'

    assert len(dao) is 1
    del dao['key']
    assert len(dao) is 0

  def test_set_dict_remove_object(self):
    dao = DictAsObject()
    dao['key']='value'

    assert len(dao) is 1
    del(dao.key)
    assert len(dao) is 0

  def test_set_object_iter_dict(self):
    dao = DictAsObject()
    dao.key = 'value'
    for key in dao:
      assert key == 'key'



