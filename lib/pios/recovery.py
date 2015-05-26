from fabric.operations import prompt
from loader import get_wrapper
from pios import run_local
import difflib, color

def print_diff(str1, str2):
  diff = difflib.ndiff(str1.splitlines(1),
                       str2.splitlines(1))


  for line in list(diff):
    if line.startswith('+'):
      with color.green():
        print line[2:]

    elif line.startswith('-'):
      with color.red():
        print line[2:]

def select_card():
  os = get_wrapper()
  prompt("\nplease remove your sd card and press enter")

  with color.for_run():
    str1 = run_local(os.list_devices())

  prompt("\nplease insert your sd card and press enter")

  with color.for_run():
    str2 = run_local(os.list_devices())

  print '+/-'
  print_diff(str1, str2)

  return prompt("\nwhich device do you want to use: ")


def select_image(msg="the image file you want to use: "):
  with color.for_run():
    run_local("ls ./images")

  return prompt('\n'+msg)

def backup(card_device=None, file_name=None):
  """store a bootable image from a sd device to ./images (run with sudo), run cd ./images && watch -n 1 'ls -al' to see changes """

  os = get_wrapper()

  if not card_device       : card_device = select_card()
  if not file_name: file_name = select_image("giva a name for the image to store under ./images/[?]: ")

  image_path = "./images/%s" % file_name

  with color.yellow():
    run_local(os.unmount(card_device))

  with color.green():
    run_local(os.dd(card_device, image_path))

def restore(card_device=None, file_name=None):
  """write a bootable image from ./images/ to sd device"""

  os = get_wrapper()

  if not card_device: card_device = select_card()
  if not file_name: file_name = select_image("the image file you want to write to %s: " % card_device)

  image_path = "./images/%s" % file_name

  with color.yellow():
    run_local(os.unmount(card_device))
    run_local(os.mk_fat_32(card_device))

  with color.green():
    run_local(os.dd(image_path, card_device))

