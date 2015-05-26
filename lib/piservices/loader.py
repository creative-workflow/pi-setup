import os, imp, sys, fabric, color

services_path = os.path.dirname(os.path.abspath(__file__))+'/../../services'

def instance(service_name):
  return load_service_module(service_name).instance

#list all possible available services as string array
def list_services(path=None):
  if not path: path = services_path
  for root, dirs, files in os.walk(path):
    return dirs

#get a PiService-Object by service name
def load_service_module(service_name):
  module_path = [services_path]
  module_info = imp.find_module(service_name, module_path)
  return imp.load_module(service_name, *module_info)

def load_fabric_tasks():
  with color.for_put():
    print 'loading services:',
    for service_name in list_services(services_path):
      print '+'+service_name,

      service = instance(service_name)

      add_task_from_service(service)

  print ""

#we need the main namespace, so fabric can find the commands
main_namespace = globals()
def set_fabric_namespace(namespace):
  global main_namespace
  main_namespace = namespace

def add_task_from_method(task_name, f, doc=''):
  namespace = main_namespace
  if doc:
    try:
      f.__func__.__doc__ = doc
    except AttributeError:
      f.__doc__ = doc
  wrapper   = fabric.api.task(name=task_name)
  namespace[task_name] = wrapper(f)

#see https://nulab-inc.com/blog/nulab/advanced-method-define-tasks-fabric/
def add_task_from_service(service):
  def call(name, *args, **kwargs):
    func = None
    try:
      func = getattr(service, name)
    except AttributeError:
      with color.for_error():
        print "Task %s::%s not found" % (service.name, name)
        sys.exit(1)

    return func(*args, **kwargs)

  add_task_from_method(service.name, call)

  import piservice

  for command in service.commands:
    func      = getattr(service, command)
    func_name = func.__name__
    color     = '33'
    if func_name in piservice.piservice_standart_commands or func_name in piservice.piservcie_managed_standart_commands:
      color = '90'

    task_name = '%s:\033[%sm%s\033[0m' % (service.name, color, func_name)

    add_task_from_method(task_name, func)

