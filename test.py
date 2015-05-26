import sys, unittest, os

sys.path.append(os.path.realpath(os.path.dirname(__file__))+'/lib')
tests_folder = os.path.realpath(os.path.dirname(__file__))+'/tests'

from tests import ConsoleTestRunner

def load_tests(loader, tests, pattern):
  suite = unittest.TestSuite()

  pattern='test_*.py'
  for dirname, dirnames, filenames in os.walk(tests_folder):
    for path in dirnames:
      path=dirname+'/'+path
      for all_test_suite in unittest.defaultTestLoader.discover(path, pattern=pattern, top_level_dir=path):
        for test_suite in all_test_suite:
          suite.addTest(test_suite)

  return suite

if __name__ == '__main__':
  os.environ['ENVIRONMENT'] = 'test'

  unittest.main(verbosity=2, exit=False, testRunner=ConsoleTestRunner)
