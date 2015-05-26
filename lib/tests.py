import unittest, os, sys
from contextlib import contextmanager
from cStringIO import StringIO


class Case(unittest.TestCase):
  @contextmanager
  def captured_output(self):
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
      sys.stdout, sys.stderr = new_out, new_err
      yield sys.stdout.getvalue(), sys.stderr
    finally:
      sys.stdout, sys.stderr = old_out, old_err

  def get_shared_fixture_path(self, name):
    return os.path.dirname(os.path.realpath(__file__))+'/tests/fixtures/'+name

  def get_fixture_path(self, name):
    return os.path.dirname(os.path.realpath(__file__))+'/../../tests/fixtures/'+name


class ConsoleTestResult(unittest.TextTestResult):
  def addSuccess(self, test):
    unittest.TestResult.addSuccess(self, test)
    print self.green('OK')

  def addError(self, test, err):
    unittest.TestResult.addError(self, test, err)
    print self.red('Exception')

  def addFailure(self, test, err):
    unittest.TestResult.addFailure(self, test, err)
    print self.red('Failed')

  def addSkip(self, test, cause):
    unittest.TestResult.addSkip(self, test, cause)
    print self.grey('Skipped')

  def getDescription(self, desc):
    return self.grey(unittest.TextTestResult.getDescription(self, desc))

  def printErrorList(self, flavour, errors):
    for test, err in errors:
      self.stream.writeln(self.separator1)
      self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
      self.stream.writeln(self.separator2)
      self.stream.writeln("%s" % self.red(err))

  def colorize(self, msg, color):
    return '\033['+color+'m '+msg+' \033[m'

  def green(self, msg):
    return self.colorize(msg, '1;32')

  def red(self, msg):
    return self.colorize(msg, '1;31')

  def grey(self, msg):
    return self.colorize(msg, '1;37')


class ConsoleTestRunner(unittest.TextTestRunner):
  def _makeResult(self):
    return ConsoleTestResult(self.stream, self.descriptions, self.verbosity)
