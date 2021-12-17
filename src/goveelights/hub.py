"""

goveelights.hub

This contains the engine for the goveelights package.

"""
import logging
<<<<<<< HEAD

GOVEE_URI_BASE = "https://developer-api.govee.com/v1"
GOVEE_URI_PATH_DEVICES = "/devices"
GOVEE_URI_PATH_STATE = f"{GOVEE_URI_PATH_DEVICES}/state"
GOVEE_URI_PATH_CONTROL = f"{GOVEE_URI_PATH_DEVICES}/control"
GOVEE_URI_DEVICES = f"{GOVEE_URI_BASE}{GOVEE_URI_PATH_DEVICES}"
GOVEE_URI_STATE = f"{GOVEE_URI_BASE}{GOVEE_URI_PATH_STATE}"
GOVEE_URI_CONTROL = f"{GOVEE_URI_BASE}{GOVEE_URI_PATH_CONTROL}"

GOVEE_DEVICE_LIST_KEY = "devices"
GOVEE_STATE_DICT_PROPERTIES = "properties"

GOVEE_BODY_DEVICE = "device"
GOVEE_BODY_MODEL = "model"
GOVEE_BODY_CMD = "cmd"
GOVEE_BODY_NAME = "name"
GOVEE_BODY_VALUE = "value"

GOVEE_DEVICE_STATE_ON = "on"
GOVEE_DEVICE_STATE_OFF = "off"
GOVEE_DEVICE_STATES = (GOVEE_DEVICE_STATE_ON, GOVEE_DEVICE_STATE_OFF)

GOVEE_CMD_TURN = "turn"
GOVEE_CMD_BRIGHT = "brightness"
GOVEE_CMD_COLOR = "color"
GOVEE_CMD_COLOR_TEMP = "colorTem"

GOVEE_BRIGHTNESS_MIN = 1
GOVEE_BRIGHTNESS_MAX = 100

GOVEE_KEY_COLOR_RED = "r"
GOVEE_KEY_COLOR_GREEN = "g"
GOVEE_KEY_COLOR_BLUE = "b"

GOVEE_COLOR_MIN = 0
GOVEE_COLOR_MAX = 255

GOVEE_KEY_ONLINE = "online"
GOVEE_KEY_POWER_STATE = "powerState"
GOVEE_KEY_BRIGHTNESS = "brightness"
GOVEE_KEY_COLOR = "color"
GOVEE_KEY_COLOR_TEMP = "colorTem"

GOVEE_POWER_ON = "on"
GOVEE_POWER_OFF = "off"
GOVEE_POWER_STATES = (GOVEE_POWER_ON, GOVEE_POWER_OFF)

logger = logging.getLogger(__name__)
#logging.basicConfig(filename='testing.log', level=logging.INFO)
=======
import logging.config

from .client import GoveeClient
from .consts import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR,
    ATTR_COLOR_TEMP,
    ATTR_POWER_STATE,
    CMD_BRIGHT,
    CMD_COLOR,
    CMD_COLOR_TEMP,
    CMD_TURN,
)
from .device import (
    GoveeDevice,
)
from .exceptions import (
    ClientException,
    DeviceException,
    GoveeHubException,
    RefreshException,

)
from .settings import LOGGING

ATTR_CMD_DICT = {
    ATTR_BRIGHTNESS: CMD_BRIGHT,
    ATTR_COLOR: CMD_COLOR,
    ATTR_COLOR_TEMP: CMD_COLOR_TEMP,
    ATTR_POWER_STATE: CMD_TURN,
}

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)

>>>>>>> 95206d1969f7285686979b827c82104c492977d7

class GoveeHub():
    """
    This hub contains all the logic to use the Govee API and supervise devices.
    """

<<<<<<< HEAD
    def __init__(self, device_class, device_client):
        logger.info(f"Creating hub")
        self._device_class = device_class
        #self.devices = {}
        self._devices = {}
        self.client = device_client
=======
    def __init__(self, device_client):
        logger.info("Creating hub")
        self.client = device_client
        self._devices = {}
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def devices(self):
        """
        This is where all devices for an account are stored.
        """
        # Need to have a request submitted if nothing is present.
        logger.info('Getting Devices for hub')
<<<<<<< HEAD
        if not self._devices:
            logger.error('Found no devices, submitting requests')
            self.get_devices()

        return self._devices

    @devices.setter
    def devices(self, devices):
        """
        This receives a tuple containing dicts with device information.
        """
        self._devices = devices
=======
        try:
            return self._devices
        except AttributeError:
            logger.warn("devices attribute is not set")
            return None
        except Exception as e:
            raise GoveeHubException.error("Failed to acces devices") from e

    def register_device(self, device):
        """
        This is used to register a device with the hub so the hub may manage it.
        """
        logger.info(f"Registering device {device.id}")
        assert issubclass(
            device.__class__, GoveeDevice
        ), "Device must be a subclass of GoveeDevice."

        try:
            self._devices[device.id] = device

            # self._devices[device.id].registered = True

            device._hub = self
        except Exception as e:
            raise GoveeHubException.error("Failed to register device") from e

    def register_devices(self, device_generator):
        for device in device_generator:
            self.register_device(device)
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def client(self):
        """
        This is the client that the hub uses to communicate with Govee.
        """
<<<<<<< HEAD
        return self._client
=======
        try:
            return self._client
        except AttributeError as ae:
            raise GoveeHubException.warn("Client not set") from ae
        except Exception as e:
            raise GoveeHubException(
                "Failed to retrieve client") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @client.setter
    def client(self, client):
        """
        This receives a GoveeClient instance.
        """
<<<<<<< HEAD
        #assert type(client) is GoveeClient, "Client must be govee_api."
        self._client = client

    #
    # Here contains methods used to retrieve data
    #

    def _get_devices(self):
        """
        This is responsible for returning a list of devices provided by the Govee API.
        """
        return self.client.get_data(GOVEE_URI_DEVICES)[GOVEE_DEVICE_LIST_KEY]

    def get_devices(self):
        """
        This is responsible for updating the devices the hub supervises.
        """

        # self._devices = {
        #     self._device_class(device_dict)
        #     for device_dict
        #     in self._get_devices()
        # }

        for device_dict in self._get_devices():
            device = self._device_class(self, device_dict=device_dict)
            self._devices[device.id] = device

    def _get_device_properties(self, device_id):
        """
        This is responsible for returning a dict of device state information from the Govee API.
        """
        return self.client.get_data(
            GOVEE_URI_STATE,
            device_id=device_id,
            model=self.devices[device_id].model
        )[GOVEE_STATE_DICT_PROPERTIES]

    def get_device_state(self, device_id):
        """
        This is used to retrieve the state of a specific Govee device.
        """
        logger.info(f"Getting state for device")


        # This is just a temp fix to make the package run successfully.
        property_list = self._get_device_properties(device_id)

        logger.info(f"Got property list: {property_list}")

        property_dict = {}
        for property in property_list:
            try:
                property_dict[GOVEE_KEY_ONLINE] = property[GOVEE_KEY_ONLINE]
                logger.info('Found Online State')
                continue
            except KeyError:
                pass

            try:
                property_dict[GOVEE_KEY_POWER_STATE] = property[GOVEE_KEY_POWER_STATE]
                logger.info('Found Power State')
                continue
            except KeyError:
                pass

            try:
                property_dict[GOVEE_KEY_BRIGHTNESS] = property[GOVEE_KEY_BRIGHTNESS]
                logger.info('Found Brightness State')
                continue
            except KeyError:
                pass

            try:
                property_dict[GOVEE_KEY_COLOR] = property[GOVEE_KEY_COLOR]
                logger.info('Found Color State')
                continue
            except KeyError:
                pass

            try:
                property_dict[GOVEE_KEY_COLOR_TEMP] = property[GOVEE_KEY_COLOR_TEMP]
                logger.info('Found Color Temp State')
                continue
            except KeyError:
                pass


        self.devices[device_id].update_state(property_dict)


    #
    # Here we have commands that interact with the API client
    #


    def set_power_state(self, device_id, power_state):
        """
        This submits the "turn" command to the device.
        """
        logger.info(f"Setting {device_id} power {power_state}")
        #assert power_state in GOVEE_POWER_STATES, f"{power_state} is an invalid power state."
        if power_state not in GOVEE_POWER_STATES:
            return

        try:
            self._send_command(device_id, GOVEE_CMD_TURN, power_state)
        except Exception as e:
            logger.error(f"Error while submitting command - {e}")
            pass

    def set_brightness(self, device_id, brightness):
        """
        This submits the "brightness" command to the device.
        """
        logger.info(f"Setting {device_id} brightness {brightness}")
        assert GOVEE_BRIGHTNESS_MIN <= brightness <= GOVEE_BRIGHTNESS_MAX, f"{brightness} is not a valid brightness level"
        try:
            self._send_command(device_id, GOVEE_CMD_BRIGHT, brightness)
        except Exception:
            pass

    def set_color(self, device_id, r=None, g=None, b=None):
        """
        This submits the "color" command to the device.
        """
        logger.info(f"Setting {device_id} color ({r}, {g}, {b})")
        try:
            self._send_command(device_id, GOVEE_CMD_COLOR, Color(r, g, b).get_dict())
        except Exception as e:
            logger.error(f"Error while submitting color - {e}")
            pass


    def set_color_temp(self, device_id, color_temp):
        """
        This submits the "colorTem" command to the device.
        """
        logger.info(f"Setting {device_id} color_temp {color_temp}")
        try:
            self._send_command(device_id, GOVEE_CMD_COLOR_TEMP, color_temp)
        except Exception:
            pass




    def _send_command(self, device_id, command, value):
        """
        This is used to control the device.
        """
        logger.info(f"Sending: {device_id} - {command} - {value}")

        # This is just a quick way to validate the corresponding device exists.
        try:
            device = self.devices[device_id]
            logger.info(f"Found device {{device_id}}")
        except KeyError:
            logger.error(f"Failed to find device {device_id}")
            return False


        assert command in device.supported_commands, f"Device does not support command {command}"


        req_body = {
            GOVEE_BODY_DEVICE: self.devices[device_id].id,
            GOVEE_BODY_MODEL: self.devices[device_id].model,
            GOVEE_BODY_CMD: {
                GOVEE_BODY_NAME: command,
                GOVEE_BODY_VALUE: value
            }
        }

        logger.info(f"Build request body: {req_body}")

        try:
            req = self.client.put_data(
                GOVEE_URI_CONTROL,
                device_id,
                self.devices[device_id].model,
                req_body
            )

        except Exception:
            return False

        else:
            logger.info(f"Got response: {req.status_code} - {req.text}")
            self.client.get_device_state(device_id) # Automativcally update the device state
            return True

class Color():
    """
    This is used to define the RGB value of a color for the light.
    """

    def __init__(self, r=None, g=None, b=None, color_dict=None):
        logger.info(f"Creating color ({r}, {g}, {b}) - {color_dict}")

        if color_dict:
            self.red, self.green, self.bluee = Color._parse_dict(color_dict)

        elif all(color is None for color in (r, g, b)):
            raise ColorException("Invalid color configuration provided.")

        else:
            self.red = r
            self.green = g
            self.blue = b


    def __eq__(self, value):
        if type(value) is dict:
            try:
                self.red = value[GOVEE_KEY_COLOR_RED]
                self.green = value[GOVEE_KEY_COLOR_GREEN]
                self.blue = value[GOVEE_KEY_COLOR_BLUE]
            except AttributeError:
                return False

            return True

        elif type(value) is Color:
            if (self.r == value.r) and (self.g == value.g) and (self.b == value.b):
                return True

            return False

        raise TypeError(f"{type(value)} is not a supported class.")


    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = Color._validate_color(value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = Color._validate_color(value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = Color._validate_color(value)

    #
    # Here are our helpers.
    #

    @staticmethod
    def _validate_color(value):
        """
        This is used to validate that the color value is acceptable.
        """

        # Treat a lack of a value as a 0
        if value is None:
            return 0

        # Make sure it's some kind of int
        try:
            value_int = int(value)
        except TypeError:
            raise ColorException(f"Cannot value as an int")

        else:
            # We have an int
            if not GOVEE_COLOR_MIN <= value_int <= GOVEE_COLOR_MAX:
                raise ColorException(f"Color value {value_int} is invalid.")

            return value

        # We shouldn't be able to get here.
        raise ColorException("Don't know how you reached here.")

    @staticmethod
    def _parse_dict(color_dict):
        try:
            return \
                color_dict[GOVEE_KEY_COLOR_RED], \
                color_dict[GOVEE_KEY_COLOR_GREEN], \
                color_dict[GOVEE_KEY_COLOR_BLUE]


        except AttributeError:
            return None

    def get_dict(self):
        return {
            GOVEE_KEY_COLOR_RED: self.red,
            GOVEE_KEY_COLOR_GREEN: self.green,
            GOVEE_KEY_COLOR_BLUE: self.blue
        }

class ColorException(Exception):
    """
    This class is used to indicate some issue was encountered with a color.
    """
=======
        if issubclass(type(client), GoveeClient):
            self._client = client
        else:
            raise GoveeHubException("Client is not a GoveeClient Subclass.")

    #
    # Here contains methods used to interface with the client
    #

    def refresh_device(self, device):
        """
        This is used to request a device's current properties from the client
        and update the device accordingly.
        A RefreshException is thrown if there's an exception encountered while
        updating the device.
        """
        logger.info(f"Refreshing device: {device.id}")

        try:
            for attr, value in self.client.get_device_state(device.id, device.model).items():
                logger.debug(f"Setting {attr} = {value}")
                setattr(device, attr, value)
        except ClientException as ce:
            raise RefreshException(
                f"Failed to fetch data: {device.id}") from ce
        except DeviceException as de:
            raise RefreshException(
                f"Failed to update: {device.id}") from de
        except Exception as e:
            raise RefreshException() from e

    def control_device(self, device, attr, value):
        """
        This is used to facilitate an API call when attempting to update
        a device.
        """
        logger.info(f"control_device: {device} - {attr} - {value}")

        try:
            if self.client.update_device_state(
                    device.id, device.model, ATTR_CMD_DICT[attr], value):
                return True
        except AttributeError as e:  # This may need to be changed.
            raise GoveeHubException(
                f"Failed to update: {device} - {attr}") from e

        return False

    #
    # Here are methods used to manage associated devices.
    #

    def build_devices(self):
        """
        This is responsible for automatically creating the devices associated
        with the hub. It requests dicts containing device information from the
        client.
        """
        self.register_devices(GoveeDevice(self, device_dict=device_dict)
                              for device_dict in self.client.get_devices())
>>>>>>> 95206d1969f7285686979b827c82104c492977d7
