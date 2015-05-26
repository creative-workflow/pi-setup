from tests import Case
from mock import patch, MagicMock, Mock, DEFAULT

class TestPiService(Case):

  def test_apt_get_instructions(self):
    with patch.multiple('fabric', tasks=DEFAULT, api=DEFAULT, operations=DEFAULT) as fabric:
      with patch.multiple('os', unlink=DEFAULT):

        from piservices import PiService
        class PiServiceWithAptGetInstructions(PiService):
          name = 'test'
          apt_get_install = ['date']

        service = PiServiceWithAptGetInstructions()
        print service.install()
