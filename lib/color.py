import sys
from contextlib import contextmanager


BLUE = 34  # https://github.com/fabric/fabric/blob/1.7/fabric/colors.py#L40
GREEN = 32
LIGHT_YELLOW = 93
YELLOW = 33
DARK_GREY = 90
RED = 31
LIGHT_GREY = 37
LIGHT_BLUE = 94


@contextmanager
def red():
  with colored_output(RED):
    yield

@contextmanager
def green():
  with colored_output(GREEN):
    yield

@contextmanager
def yellow():
  with colored_output(YELLOW):
    yield

@contextmanager
def light_yellow():
  with colored_output(LIGHT_YELLOW):
    yield

@contextmanager
def light_grey():
  with colored_output(LIGHT_GREY):
    yield

@contextmanager
def dark_grey():
  with colored_output(DARK_GREY):
    yield

@contextmanager
def blue():
  with colored_output(BLUE):
    yield

@contextmanager
def light_blue():
  with colored_output(LIGHT_BLUE):
    yield




@contextmanager
def for_put():
  with colored_output(DARK_GREY):
    yield

@contextmanager
def for_get():
  with colored_output(GREEN):
    yield

@contextmanager
def for_run():
  with colored_output(YELLOW):
    yield

@contextmanager
def for_error():
  with colored_output(RED):
    yield

@contextmanager
def colored_output(color):
  sys.stdout.write("\033[%sm" % color)
  yield
  sys.stdout.write("\033[0m")
