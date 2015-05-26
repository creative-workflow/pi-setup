#!/usr/bin/python
from fabric.api import env
import sys, fabric, os

#append lib path
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/lib')

import piservices, config

#load config
env.config = config.get()

#merge febric section from config
env.update(config.get('fabric'))


@fabric.api.task(default=True)
def help():
  print "run in your prompt$: fab <command>[:argument[,argument[,...]]]"
  fabric.operations.local('fab -l')

test_file = os.path.realpath(os.path.dirname(__file__))+'/test.py'
@fabric.api.task
def test():
  cmd = 'python %s' % test_file
  if piservices.PiServicePolicies.is_local():
    fabric.operations.local(cmd)
  else:
    fabric.api.run(cmd)

@fabric.api.task
def pi(host=None, user=None, password=None):
  """give the target host(your pi) with pi:[your-pi-ip] or pi:[your-pi-ip],[user],[pass]"""

  #set default host from config
  if not host: host = config.get('stages').default

  #load default config from given host
  if host in config.get('stages'):
    env.update(config.get('stages')[host])
  else:
    #override with given values
    if host:     env.hosts    = [host]
    if user:     env.user     = user
    if password: env.password = password

@fabric.api.task
def run(command="ls -la"):
  """run a command on local or pi run:'ls -al'"""
  if piservices.PiServicePolicies.is_local():
    fabric.operations.local(command)
  else:
    fabric.api.run(command)


#bootstrap
piservices.set_fabric_namespace(globals())

piservices.load_fabric_tasks()
