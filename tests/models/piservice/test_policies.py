from tests import Case
from fabric.api import env
from piservices import PiServicePolicies

class TestPolicies(Case):
  def test_detect_local_from_fabric_env_vars(self):
    env.hosts = None
    self.assertTrue(PiServicePolicies.is_local())


    for stage in ['localhost', '127.0.0.1', '::1']:
      env.hosts = [stage]
      self.assertTrue(PiServicePolicies.is_local())

    env.hosts = ['192.168.0.1']
    self.assertFalse(PiServicePolicies.is_local())

