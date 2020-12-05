import pyvisa
import mock 
from src.equipments.lab_equipment import BK8600


class TestBk8600(object):
    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_constructor(self, mock_pyvisa):
        # given
        resource_id = "USB0::65535"
        resource_manager = mock_pyvisa.ResourceManager.return_value
        instrument = resource_manager.open_resource.return_value

        # when
        BK8600(resource_id)

        # then
        instrument.write.assert_called_with("*RST")
        instrument.query.assert_called_with("*IDN?")
        resource_manager.open_resource.assert_called_with(resource_id)

    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_set_current(self, mock_pyvisa):
        # given
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        current_a = 1
        instrument = BK8600()
        py_instrument.reset_mock()

        # when
        instrument.set_current(current_a)

        # then
        py_instrument.write.assert_has_calls([
            call("{} {}".format("CURR:LEV", current_a)),
            call("INPut ON")
        ])
        py_instrument.query.assert_called_with("*OPC?")

    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_toggle_eload_true(self, mock_pyvisa):
        # given
        state = True
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = BK8600()
        py_instrument.reset_mock()

        # when
        instrument.toggle_eload(state)

        # then
        py_instrument.write.assert_has_calls([
            call("INPut ON")
        ])

    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_toggle_eload_false(self, mock_pyvisa):
        # given
        state = False
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = BK8600()
        py_instrument.reset_mock()

        # when
        instrument.toggle_eload(state)

        # then
        py_instrument.write.assert_has_calls([
            call("INPut OFF")
        ])

    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_measure_voltage(self, mock_pyvisa):
        # given
        voltage = 30
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = BK8600()
        py_instrument.reset_mock()
        py_instrument.query.return_value = voltage

        # when
        v = instrument.measure_voltage()

        # then
        py_instrument.query.assert_called_with("MEAS:VOLT:DC?")
        assert v == voltage

    @patch("{}.{}".format(BK8600.__module__, pyvisa.__name__))
    def test_measure_current(self, mock_pyvisa):
        # given
        current = 30
        py_instrument = mock_pyvisa.ResourceManager.return_value.open_resource.return_value
        instrument = BK8600()
        py_instrument.reset_mock()
        py_instrument.query.return_value = current

        # when
        c = instrument.measure_current()

        # then
        py_instrument.query.assert_called_with("MEAS:CURR:DC?")
        assert c == current
