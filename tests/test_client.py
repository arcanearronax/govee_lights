"""
This is used to validate the client functions as expected.
"""

import warnings

import unittest

from src.goveelights.client import (
    GoveeClient,
    HEADER_API_KEY,
    HEADER_CONTENT_TYPE,
    HEADER_CONTENT_TYPE_VALUE,
    URI_DEVICES,
    URI_CONTROL,
    URI_STATE,
)
from src.goveelights.client import (
    QUERY_DEVICE,
    QUERY_MODEL,
)
from src.goveelights.color import (
    Color,
    COLOR_MAX,
    COLOR_MIN
)
from src.goveelights.consts import (
    ATTR_ID,
    ATTR_MODEL,
    ATTR_ONLINE,
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_RANGE,
    ATTR_CONTROL,
    ATTR_DEVICE_NAME,
    ATTR_POWER_STATE,
    ATTR_RETRIEVE,
    ATTR_SUPPORTED_COMMANDS,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    CMD_TURN,
    CMD_BRIGHT,
    CMD_COLOR,
    CMD_COLOR_TEMP,
    KEY_CODE,
    KEY_DATA,
    KEY_DEVICES,
    KEY_MESSAGE,
    KEY_RED,
    KEY_GREEN,
    KEY_BLUE,
    POWER_ON,
    POWER_OFF,
)
from src.goveelights.exceptions import InvalidAPIKey
from .conftest import (
    API_KEY_GOOD,
    API_KEY_BAD,
    API_KEY_INVALID,
    API_KEY_NONE,
    DEVICE_ID_VALID,
    DEVICE_MODEL_GOOD
)

COLOR_RED = Color(red=COLOR_MAX, green=COLOR_MIN, blue=COLOR_MIN)
COLOR_GREEN = Color(red=COLOR_MIN, green=COLOR_MAX, blue=COLOR_MIN)
COLOR_BLUE = Color(red=COLOR_MIN, green=COLOR_MIN, blue=COLOR_MAX)
RGB_RED = COLOR_RED.rgb_dict()
RGB_BLUE = COLOR_BLUE.rgb_dict()
RGB_GREEN = COLOR_GREEN.rgb_dict()


class TestCreate(unittest.TestCase):
    """
    This is the class used to manage our test cases for the client.
    """

    def setUp(self):
        """
        This is used to set up data prior to running tests.
        """

    def tearDown(self):
        """
        This is used to clean up data after tests.
        """

    def test_create_client_key_good(self):
        """
        This is used to validate that a client is created as expected.
        """
        good_client = GoveeClient(API_KEY_GOOD)
        self.assertEqual(good_client.api_key, API_KEY_GOOD)

    def test_create_client_key_bad(self):
        """
        This is used to validate that a client can be created with a bad API
        key. Bad API keys should be caught during validation.
        """
        with self.assertRaises(InvalidAPIKey):
            GoveeClient(API_KEY_BAD)

    def test_create_client_key_invalid(self):
        """
        This is used to validate that a client cannot be created with an
        Invalid API key.
        """
        with self.assertRaises(InvalidAPIKey):
            GoveeClient(API_KEY_INVALID)

    def test_create_client_key_none(self):
        """
        This is used to validate that a client can be created without a key.
        """
        with self.assertRaises(InvalidAPIKey):
            GoveeClient(API_KEY_NONE)


# @pytest.mark.usefixtures("govee_client")
# class TestClientRequestBuildProcess(unittest.TestCase):
class TestHeaders(unittest.TestCase):
    """
    This class is used to manage test cases related to building requests which
    are sent to the API.
    """

    def setUp(self):
        """
        This is used to clean up data after running tests.
        """

    def tearDown(self):
        """
        This is used to clean up data after running tests.
        """

    def test_headers(self):
        """
        This is used to validate headers are built correctly.
        """
        client = GoveeClient(API_KEY_GOOD)
        headers = client._generate_headers()
        self.assertIn(HEADER_API_KEY, headers)
        self.assertEqual(headers[HEADER_API_KEY], client.api_key)
        self.assertEqual(headers[HEADER_CONTENT_TYPE],
                         HEADER_CONTENT_TYPE_VALUE)


class TestParameters(unittest.TestCase):

    def setUp(self):
        """
        This is used to set up data after running tests.
        """

    def tearDown(self):
        """
        This is used to clean up data after running tests.
        """

    def test_parameters_good(self):
        """
        This is used to validate that parameters are built correctly.
        """
        parameters = GoveeClient._generate_params(
            DEVICE_ID_VALID, DEVICE_MODEL_GOOD)
        self.assertIn(QUERY_DEVICE, parameters)
        self.assertEqual(DEVICE_ID_VALID, parameters[QUERY_DEVICE])
        self.assertIn(QUERY_MODEL, parameters)
        self.assertEqual(DEVICE_MODEL_GOOD, parameters[QUERY_MODEL])

    def test_parameters_none(self):
        """
        This is used to validate that None is returned when values aren't
        passed when params are generated.
        """
        parameters = GoveeClient._generate_params()
        self.assertIsNone(parameters, "Parameters must return None")


class TestGetRequests(unittest.TestCase):

    def setUp(self):
        """
        This is used to set up data after running tests.
        """
        self.client = GoveeClient(API_KEY_GOOD)

    def tearDown(self):
        """
        This is used to clean up data after running tests.
        """

    def test_get_devices(self):
        """
        This is used to validate that the client can successfully request
        devices via the API.
        """
        device_list = self.client.get_devices()
        self.assertIsInstance(
            device_list, list, "get_devices must return a list")

        for device in device_list:
            self.assertIn(ATTR_ID, device)
            self.assertIn(ATTR_MODEL, device)
            self.assertIn(ATTR_DEVICE_NAME, device)
            self.assertIn(ATTR_CONTROL, device)
            self.assertIn(ATTR_RETRIEVE, device)
            self.assertIn(ATTR_SUPPORTED_COMMANDS, device)
            self.assertIn(ATTR_COLOR_TEMP_RANGE, device)

    def test_get_device_state(self):
        """
        This is used to validate that the client can successfully request
        device properties.
        """
        device_list = self.client.get_devices()
        for device in device_list:
            device_data = self.client.get_device_state(
                device[ATTR_ID], device[ATTR_MODEL])
            self.assertIn(ATTR_ID, device_data)
            self.assertIn(ATTR_MODEL, device_data)
            self.assertIn(ATTR_ONLINE, device_data)
            self.assertIn(ATTR_POWER_STATE, device_data)
            self.assertIn(ATTR_BRIGHTNESS, device_data)


class TestPutRequests(unittest.TestCase):

    def setUp(self):
        """
        This is used to set up data after running tests.
        """
        self.client = GoveeClient(API_KEY_GOOD)
        self.devices = self.client.get_devices()

    def tearDown(self):
        """
        This is used to clean up data after running tests.
        """

    def set_power_state(self, device_id, device_model, power_state):
        """
        This is used to provide a centralized method to update device power
        states.

        This validates the code and message received in the response.
        """
        if self.client.update_device_state(
                device_id, device_model, CMD_TURN, power_state):
            pass
        else:
            raise AssertionError(f"Failed to set power state: {power_state}")

    def set_brightness_state(self, device_id, device_model, brightness):
        """
        This is used to set the brighness of a govee device.
        """
        if self.client.update_device_state(device_id, device_model, CMD_BRIGHT, brightness):
            pass
        else:
            raise AssertionError(f"Failed to set brightness: {brightness}")

    def set_color_state(self, device_id, device_model, color):
        """
        This is used to set the color of a govee device.
        """
        if self.client.update_device_state(
                device_id, device_model, CMD_COLOR, color):
            pass
        else:
            raise AssertionError(f"Failed to set color: {color}")

    def set_color_temp_state(self, device_id, device_model, color_temp):
        """
        This is used to set the color temp of a govee device.
        """
        if self.client.update_device_state(device_id, device_model, CMD_COLOR_TEMP, color_temp):
            pass
        else:
            raise AssertionError(f"Failed to set color temp: {color_temp}")

    def test_cmd_power_off(self):
        """
        This is used to validate devices can be turned on.
        """
        for device in self.devices:
            self.set_power_state(
                device[ATTR_ID], device[ATTR_MODEL], POWER_OFF)

    def test_cmd_power_on(self):
        """
        This is used to validate devices can be turned on.
        """
        for device in self.devices:
            self.set_power_state(
                device[ATTR_ID], device[ATTR_MODEL], POWER_ON)

    def test_cmd_brightness_min(self):
        """
        This is used to test updating device brightness.
        """
        for device in self.devices:
            self.set_brightness_state(
                device[ATTR_ID], device[ATTR_MODEL], BRIGHTNESS_MIN)

    def test_cmd_brightness_max(self):
        """
        This is used to test updating device brightness.
        """
        for device in self.devices:
            self.set_brightness_state(
                device[ATTR_ID], device[ATTR_MODEL], BRIGHTNESS_MAX)

    def test_cmd_color_rgb_red(self):
        """
        This is used to validate the RGB color red can be set.
        """
        for device in self.devices:
            self.set_color_state(device[ATTR_ID], device[ATTR_MODEL], RGB_RED)

    def test_cmd_color_rgb_green(self):
        """
        This is used to validate a color can be set appropriately.
        """
        for device in self.devices:
            self.set_color_state(
                device[ATTR_ID], device[ATTR_MODEL], RGB_GREEN)

    def test_cmd_color_rgb_blue(self):
        """
        This is used to validate a color can be set appropriately.
        """
        for device in self.devices:
            self.set_color_state(
                device[ATTR_ID], device[ATTR_MODEL], RGB_BLUE)

    def test_cmd_color_temp_min(self):
        """
        This is used to validate a device's color temp can be set
        appropriately.
        """
        for device in self.devices:
            self.set_color_temp_state(
                device[ATTR_ID], device[ATTR_MODEL], device[ATTR_COLOR_TEMP_RANGE][0])

    def test_cmd_color_temp_max(self):
        """
        This is used to validate a device's color temp can be set
        appropriately.
        """
        for device in self.devices:
            self.set_color_temp_state(
                device[ATTR_ID], device[ATTR_MODEL], device[ATTR_COLOR_TEMP_RANGE][1])
