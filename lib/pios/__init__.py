import subprocess

def run_local(cmd):
  print '>> '+cmd
  ret = subprocess.check_output(cmd, shell=True)
  print ret
  return ret
