'''
Basic Testcase Example.
'''
from tests import Case

'''called once if the module is loaded'''
def setUpModule():
  pass


class TestTests(Case):
  '''called once if the class is instanciated'''
  @classmethod
  def setUpClass(cls):
    pass

  '''called before each test'''
  def setUp(self):
    pass

  '''test method it self starts with test_...'''
  def test_call(self):
    self.assertTrue(True)

  '''called after each test'''
  def tearDown(self):
    pass

  '''called before destroying the stest case'''
  @classmethod
  def tearDownClass(cls):
    pass

'''called once if the module is unloaded'''
def tearDownModule():
  pass
