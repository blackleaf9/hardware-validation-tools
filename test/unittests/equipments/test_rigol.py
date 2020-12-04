import pyvisa
from mock import patch, call
from src.equipments.rigol import DS1054Z


class TestDS1054Z(object):
    @patch("{}.{}".format(DS1054Z.__module__, pyvisa.__name__))
    def test_constructor(self, mock_pyvisa):
        # given
        resource_id = "USB0::65535"
        resource_manager = mock_pyvisa.ResourceManager.return_value
        instrument = resource_manager.open_resource.return_value

        # when
        DS1054Z(resource_id)

        # then
        instrument.write.assert_called_with("*RST")
        instrument.query.assert_called_with("*IDN?")
        resource_manager.open_resource.assert_called_with(resource_id)
