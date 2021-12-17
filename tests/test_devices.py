import unittest

from src.goveelights.client import GoveeClient
from src.goveelights.color import (
    Color,
    COLOR_MAX,
    COLOR_MIN,
)
from src.goveelights.consts import (
    SUPPORTED_COMMANDS,
    KEY_DEVICE,
    KEY_MODEL,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    POWER_ON,
    POWER_OFF,
)
from src.goveelights.device import (
    GoveeDevice,
)
from src.goveelights.exceptions import (
    DeviceException,
    InvalidValue,
)
from src.goveelights.hub import GoveeHub

from .conftest import (
    API_KEY_GOOD,
    DEVICE_DATA_GOOD,
    DEVICE_NAME_GOOD,
    DEVICE_MODEL_GOOD,
    DEVICE_ID_GOOD,
    DEVICE_ID_BAD,
    DEVICE_ID_INVALID,
    DEVICE_ID_NONE,
    DEVICE_ID_VALID,
    DEVICE_DATA_NO_DEVICE,
    DEVICE_DATA_NO_MODEL,
    DEVICE_DATA_NO_DEVICE_NAME,
    DEVICE_DATA_NO_CONTROL,
    DEVICE_DATA_NO_RETRIEVE,
    DEVICE_DATA_NO_SUPPORTED_COMMANDS,
    DEVICE_DATA_NO_PROPERTIES,
    DEVICE_CONTROL_GOOD,
    DEVICE_RETRIEVE_GOOD,
    TEMP_RANGE_MIN_GOOD,
    TEMP_RANGE_MAX_GOOD,
    ALLOWED_MODES_ALL,
    ALLOWED_MODES_SOME,
    ALLOWED_MODES_BAD,
    ALLOWED_MODES_NONE,
)


class TestCreateDeviceHub(unittest.TestCase):
    """
    This is used to manage device creation tests.
    """

    def setUp(self):
        """
        This is used to setup the tests.
        """

    def tearDown(self):
        """
        This is used to clean up after the tests.
        """

    def test_create_device_hub_only(self):
        """
        This is used to valid ate devices can be created.
        """
        client = GoveeClient(API_KEY_GOOD)
        hub = GoveeHub(client)
        with self.assertRaises(DeviceException):
            GoveeDevice(hub)


class TestCreateDeviceID(unittest.TestCase):
    """
    This is used to manage device creation tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to set up the class before testing.
        """
        client = GoveeClient(API_KEY_GOOD)
        cls.hub = GoveeHub(client)

    def setUp(self):
        """
        This is used to setup the tests.
        """
        self.hub = type(self).hub

    def tearDown(self):
        """
        This is used to clean up after the tests.
        """

    def test_create_device_id_valid(self):
        """
        This is used to validate devices can be created.
        """
        device = GoveeDevice(device_id=DEVICE_ID_VALID)
        self.assertIsNone(device.hub)
        self.assertEqual(device.id, DEVICE_ID_VALID, "Device ID mismatch")

    def test_create_device_id_invalid(self):
        """
        This is used to validate devices can be created.
        """
        with self.assertRaises(DeviceException):
            GoveeDevice(self.hub, DEVICE_ID_INVALID)

    def test_create_device_id_bad(self):
        """
        This is used to validate devices can be created.
        """
        with self.assertRaises(DeviceException):
            GoveeDevice(self.hub, DEVICE_ID_BAD)

    def test_create_device_id_none(self):
        """
        This is used to validate devices can be created.
        """
        with self.assertRaises(DeviceException):
            GoveeDevice(self.hub, DEVICE_ID_NONE)


class TestCreateDeviceDict(unittest.TestCase):
    """
    This is used to manage device creation tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to set up the class before testing.
        """
        client = GoveeClient(API_KEY_GOOD)
        cls.hub = GoveeHub(client)

    def setUp(self):
        """
        This is used to setup the tests.
        """
        self.hub = type(self).hub

    def tearDown(self):
        """
        This is used to clean up after the tests.
        """

    def test_create_device_dict_valid(self):
        """
        This is used to validate devices can be created.
        """
        device = GoveeDevice(self.hub, device_dict=DEVICE_DATA_GOOD)
        self.assertIs(device.hub, self.hub, "Hub mismatch found")

        self.assertEqual(device.id, DEVICE_ID_VALID)
        self.assertEqual(device.model, DEVICE_MODEL_GOOD)
        self.assertEqual(device.device_name, DEVICE_NAME_GOOD)
        self.assertEqual(device.controllable, DEVICE_CONTROL_GOOD)
        self.assertEqual(device.retrievable, DEVICE_RETRIEVE_GOOD)
        self.assertEqual(device.supported_commands, SUPPORTED_COMMANDS)
        self.assertEqual(device.color_temp_range[0], TEMP_RANGE_MIN_GOOD)
        self.assertEqual(device.color_temp_range[1], TEMP_RANGE_MAX_GOOD)


class TestProperties(unittest.TestCase):
    """
    This is used to manage tests regarding device properties.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to set up the class before testing.
        """
        client = GoveeClient(API_KEY_GOOD)
        cls.hub = GoveeHub(client)
        cls.device_data = client.get_devices()[0]

    def setUp(self):
        """
        This is used to setup the tests.
        """
        # self.device = GoveeDevice(
        #     type(self).hub, device_dict=type(self).device_data)
        self.device = GoveeDevice(
            type(self).hub, device_id=DEVICE_ID_GOOD
        )

    def tearDown(self):
        """
        This is used to clean up after a test.
        """

    def test_initialized_cycle(self):
        """
        This is used to validate the device initialized flag can be set.
        """
        self.assertTrue(self.device.initialized)

        self.device.initialized = False
        self.assertFalse(self.device.initialized)

        self.device.initialized = True
        self.assertTrue(self.device.initialized)

    def test_online_cycle(self):
        """
        This is used to validate the device online flag can be set.
        """
        self.assertIsNone(self.device.online)
        self.device.online = True
        self.assertTrue(self.device.online)
        self.device.online = False
        self.assertFalse(self.device.online)

    def test_allowed_modes_cycle(self):
        """
        This is used to validate the device allowed modes can be set.
        """
        self.assertEqual(self.device.allowed_modes, ALLOWED_MODES_NONE)
        self.device.allowed_modes = ALLOWED_MODES_ALL
        self.assertEqual(self.device.allowed_modes, ALLOWED_MODES_ALL)
        self.device.allowed_modes = ALLOWED_MODES_SOME
        self.assertEqual(self.device.allowed_modes, ALLOWED_MODES_SOME)

        with self.assertRaises(InvalidValue):
            self.device.allowed_modes = ALLOWED_MODES_BAD

        self.device.allowed_modes = ALLOWED_MODES_NONE
        self.assertEqual(self.device.allowed_modes, ALLOWED_MODES_NONE)

    def test_registered_hub(self):
        """
        This is used to validate the device registration flag works.
        """
        self.assertTrue(self.device.registered)

    def test_registered_no_hub(self):
        """
        This is used to validate the device registration flag works.
        """
        device = GoveeDevice(None, device_id=DEVICE_ID_GOOD)
        self.assertFalse(device.registered)


class TestUninitializedDevice(unittest.TestCase):
    """
    This is used to manage tests for an uninitialized device.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to set up the class before testing.
        """
        client = GoveeClient(API_KEY_GOOD)
        cls.hub = GoveeHub(client)
        cls.device_data = client.get_devices()[0]

    def setUp(self):
        """
        This is used to setup the tests.
        """
        self.device = GoveeDevice(
            type(self).hub, device_id=DEVICE_ID_VALID, initialized=False
        )
        self.device.color_temp_range = (
            TEMP_RANGE_MIN_GOOD, TEMP_RANGE_MAX_GOOD)

    def tearDown(self):
        """
        This is used to clean up after a test.
        """

    def test_power_cycle(self):
        """
        This is used to validate the device power_state flag can be set.
        """
        self.assertIsNone(self.device.power_state)
        self.device.power_state = POWER_ON
        self.assertEqual(self.device.power_state, POWER_ON)
        self.device.power_state = POWER_OFF
        self.assertEqual(self.device.power_state, POWER_OFF)

    def test_brightness_cycle(self):
        """
        This is used to validate the device brightness can be set.
        """
        self.assertIsNone(self.device.brightness)
        self.device.brightness = BRIGHTNESS_MAX
        self.assertEqual(self.device.brightness, BRIGHTNESS_MAX)
        self.device.brightness = BRIGHTNESS_MIN
        self.assertEqual(self.device.brightness, BRIGHTNESS_MIN)

    def test_color_rgb_cycle(self):
        """
        This is used to validate the device color can be set.
        """
        self.assertIsNone(self.device.color)

        red = Color(red=COLOR_MAX, blue=COLOR_MIN, green=COLOR_MIN)
        self.device.color = red
        self.assertEqual(self.device.color, red)

        green = Color(red=COLOR_MIN, blue=COLOR_MIN, green=COLOR_MAX)
        self.device.color = green
        self.assertEqual(self.device.color, green)

        blue = Color(red=COLOR_MIN, blue=COLOR_MAX, green=COLOR_MIN)
        self.device.color = blue
        self.assertEqual(self.device.color, blue)

        with self.assertRaises(InvalidValue):
            self.device.color = BRIGHTNESS_MAX

        with self.assertRaises(InvalidValue):
            self.device.color = None

    def test_color_temp_cycle(self):
        """
        This is used to validate the device color_temp can be set.
        """
        self.assertIsNone(self.device.color_temp)

        self.device.color_temp = TEMP_RANGE_MIN_GOOD
        self.assertEqual(self.device.color_temp, TEMP_RANGE_MIN_GOOD)

        self.device.color_temp = TEMP_RANGE_MIN_GOOD
        self.assertEqual(self.device.color_temp, TEMP_RANGE_MIN_GOOD)

        with self.assertRaises(InvalidValue):
            self.device.color_temp = TEMP_RANGE_MAX_GOOD + 1

        with self.assertRaises(InvalidValue):
            self.device.color_temp = 's'

        with self.assertRaises(InvalidValue):
            self.device.color_temp = None


class TestInitializedDevice(unittest.TestCase):
    """
    This is used to manage tests for an initialized device.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to set up the class before testing.
        """
        cls.client = GoveeClient(API_KEY_GOOD)

    def setUp(self):
        """
        This is used to setup the tests.
        """
        self.hub = GoveeHub(type(self).client)
        self.hub.build_devices()
        self.device = self.hub.devices[DEVICE_ID_GOOD]

    def tearDown(self):
        """
        This is used to clean up after a test.
        """
        del self.device
        del self.hub

    def test_power_cycle(self):
        """
        This is used to validate the device power_state flag can be set.
        """
        self.assertIsNone(self.device.power_state)
        self.device.power_state = POWER_ON
        self.assertEqual(self.device.power_state, POWER_ON)
        self.device.power_state = POWER_OFF
        self.assertEqual(self.device.power_state, POWER_OFF)

    def test_brightness_cycle(self):
        """
        This is used to validate the device brightness can be set.
        """
        self.assertIsNone(self.device.brightness)
        self.device.brightness = BRIGHTNESS_MAX
        self.assertEqual(self.device.brightness, BRIGHTNESS_MAX)
        self.device.brightness = BRIGHTNESS_MIN
        self.assertEqual(self.device.brightness, BRIGHTNESS_MIN)

    def test_color_cycle(self):
        """
        This is used to validate the device color can be set.
        """
        self.assertIsNone(self.device.color)

        red = Color(red=COLOR_MAX, blue=COLOR_MIN, green=COLOR_MIN)
        self.device.color = red
        self.assertEqual(self.device.color, red)

        green = Color(red=COLOR_MIN, blue=COLOR_MIN, green=COLOR_MAX)
        self.device.color = green
        self.assertEqual(self.device.color, green)

        blue = Color(red=COLOR_MIN, blue=COLOR_MAX, green=COLOR_MIN)
        self.device.color = blue
        self.assertEqual(self.device.color, blue)

        with self.assertRaises(InvalidValue):
            self.device.color = BRIGHTNESS_MAX

        with self.assertRaises(InvalidValue):
            self.device.color = None

    def test_color_temp_cycle(self):
        """
        This is used to validate the device color_temp can be set.
        """
        self.assertIsNone(self.device.color_temp)

        self.device.color_temp = TEMP_RANGE_MIN_GOOD
        self.assertEqual(self.device.color_temp, TEMP_RANGE_MIN_GOOD)

        self.device.color_temp = TEMP_RANGE_MIN_GOOD
        self.assertEqual(self.device.color_temp, TEMP_RANGE_MIN_GOOD)

        with self.assertRaises(InvalidValue):
            self.device.color_temp = TEMP_RANGE_MAX_GOOD + 1

        with self.assertRaises(InvalidValue):
            self.device.color_temp = 's'

        with self.assertRaises(InvalidValue):
            self.device.color_temp = None
