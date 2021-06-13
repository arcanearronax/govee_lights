"""
goveelights.device

This is the base class for Govee devices that use the API.

"""
import re
import logging

from .hub import (
    GOVEE_CMD_TURN,
    GOVEE_CMD_BRIGHT,
    GOVEE_CMD_COLOR,
    GOVEE_CMD_COLOR_TEMP,
    GOVEE_KEY_ONLINE,
    GOVEE_KEY_POWER_STATE,
    GOVEE_KEY_BRIGHTNESS,
    GOVEE_KEY_COLOR,
    GOVEE_KEY_COLOR_TEMP
)

GOVEE_SUPPORTED_COMMANDS = [
    GOVEE_CMD_TURN,
    GOVEE_CMD_BRIGHT,
    GOVEE_CMD_COLOR,
    GOVEE_CMD_COLOR_TEMP
]

REGEX_DEVICE_ID = "^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){7}$"

GOVEE_ONLINE_TRUE = True
GOVEE_ONLINE_FALSE = False
GOVEE_ONLINE_STATES = (GOVEE_ONLINE_TRUE, GOVEE_ONLINE_FALSE)

GOVEE_SUPPORTED_MODELS = [
    "H6160", "H6163", "H6104", "H6109", "H6110", "H6117", "H6159", "H7022", "H6086", "H6089", "H6182", "H6085", "H7014", "H5081", "H6188", "H6135", "H6137", "H6141", "H6142", "H6195", "H7005", "H6083", "H6002", "H6003", "H6148", "H6052", "H6143", "H6144", "H6050", "H6199", "H6054", "H5001", "H6050", "H6154", "H6143", "H6144", "H6072", "H6121", "H611A", "H5080", "H6062", "H614C", "H615A", "H615B", "H7020", "H7021", "H614D", "H611Z", "H611B", "H611C", "H615C", "H615D", "H7006", "H7007", "H7008", "H7012", "H7013"
]

GOVEE_KEY_DEVICE = "device"
GOVEE_KEY_MODEL = "model"
GOVEE_KEY_NAME = "deviceName"
GOVEE_KEY_CONTROL = "controllable"
GOVEE_KEY_RETRIEVE = "retrievable"
GOVEE_KEY_SUPPORTED_COMMANDS = "supportCmds"
GOVEE_KEY_PROPERTIES = "properties"

GOVEE_KEY_RANGE = "range"
GOVEE_KEY_RANGE_MIN = "min"
GOVEE_KEY_RANGE_MAX = "max"

logger = logging.getLogger(__name__)
#logging.basicConfig(filename='testing.log', level=logging.INFO)

class GoveeDevice():
    """
    This is the base class for an API compatible Govee device. This is the digital representation of the physical device.
    """

    def __init__(self, device_hub, device_id=None, device_dict=None):
        """
        The user may create an instance by providing a device ID or a dict containing the device info, provided by Govee.
        """

        logger.info(f"Creating device - id: {device_id} - dict: {device_dict}")

        if device_id: # In case we need to manually create a device
            try:
                self.id = device_id
            except Exception:
                pass
            else:
                device_hub.register_device(self)

            logger.info('Finished via id')
        elif device_dict: # We're creating a device from Govee data
            # Pull out device information from the dict
            self.id = device_dict[GOVEE_KEY_DEVICE]
            self.model = device_dict[GOVEE_KEY_MODEL]
            self.device_name = device_dict[GOVEE_KEY_NAME]
            self.controllable = device_dict[GOVEE_KEY_CONTROL]
            self.retrievable = device_dict[GOVEE_KEY_RETRIEVE]
            self.supported_commands = device_dict[GOVEE_KEY_SUPPORTED_COMMANDS]
            self.color_temp_range = (
                device_dict[GOVEE_KEY_PROPERTIES][GOVEE_KEY_COLOR_TEMP][GOVEE_KEY_RANGE][GOVEE_KEY_RANGE_MIN],
                device_dict[GOVEE_KEY_PROPERTIES][GOVEE_KEY_COLOR_TEMP][GOVEE_KEY_RANGE][GOVEE_KEY_RANGE_MAX]
            )
            logger.info('Finished parsing the dict')
        else:
            pass


    #
    # These are Govee device properties
    #

    @property
    def id(self):
        """
        This is the unique ID used to identify the device. Govee identifies it as the MAC address, but it has 8 octets.
        """
        return self._device_id

    @id.setter
    def id(self, device_id):

        def validate_device_id(device_id):
            """
            This is used to validate that the device_id meets the Govee format. If it does, device_id is returned, None otherwise.
            """

            if re.match(REGEX_DEVICE_ID, device_id):
                return device_id

            return None

        self._device_id = validate_device_id(device_id)

    @property
    def model(self):
        try:
            return self._model
        except AttributeError:
            return None

    @model.setter
    def model(self, model_name):
        assert model_name in GOVEE_SUPPORTED_MODELS, f"Model {model_name} is not supported."
        self._model = model_name

    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, device_name):
        self._device_name = device_name

    @property
    def controllable(self):
        try:
            return self._controllable
        except AttributeError:
            return None

    @controllable.setter
    def controllable(self, is_controllable=True):
        try:
            self._controllable = bool(is_controllable)
        except Exception:
            self._controllable = False

    @property
    def retrievable(self):
        try:
            return self._retrievable
        except AttributeError:
            return None

    @retrievable.setter
    def retrievable(self, is_retrievable=True):
        try:
            self._retrievable = bool(is_retrievable)
        except Exception:
            self._retrievable = False

    @property
    def supported_commands(self):
        return self._supported_commands

    @supported_commands.setter
    def supported_commands(self, command_iterable):
        """
        This is responsible for reading in supported commands for an iterable.
        """
        logger.info(f"Command iterable: {command_iterable}")
        self._supported_commands = [
            x for
            x in command_iterable
            if x in GOVEE_SUPPORTED_COMMANDS
        ]

    @property
    def color_temp_range(self):
        """
        The permitted range of color temperatures
        """
        return self._color_temp_range

    @color_temp_range.setter
    def color_temp_range(self, range_tuple):
        """
        The permitted range of color temperatures
        """

        for i in range_tuple:
            assert i >= 0, f"Invalid temperature in range - {i}"

        assert range_tuple[0] <= range_tuple[1], f"Invalid temperature range"

        self._color_temp_range = range_tuple

    #
    # Device state information below here
    #

    @property
    def online(self):
        try:
            return self._online
        except AttributeError:
            return False

    @online.setter
    def online(self, is_online=True):
        try:
            self._online = bool(is_online)
        except Exception:
            self._online = False

    @property
    def power_state(self):
        try:
            return self._power_state
        except AttributeError:
            return GOVEE_POWER_OFF

    @power_state.setter
    def power_state(self, power_state):
        self._power_state = power_state

    @property
    def brightness(self):
        try:
            return self._brightness
        except Exception:
            return None

    @brightness.setter
    def brightness(self, brightness):
        self._brightness = brightness

    @property
    def color(self):
        return self._color

    @property
    def color_temp(self):
        return self._color_temp

    @color_temp.setter
    def color_temp(self, color_temp):

        self._color_temp = color_temp


    #
    # Here we have methods for internal use
    #


    def update_state(self, state_dict):
        """
        This receives a dict and updates this device's state information.
        """
        self.online = state_dict[GOVEE_KEY_ONLINE]
        self.power_state = state_dict[GOVEE_KEY_POWER_STATE]
        self.brightness = state_dict[GOVEE_KEY_BRIGHTNESS]

        # This is where we handle ensuring we have a state.
        got_some_value = 0
        try:
            self.color_temp = state_dict[GOVEE_KEY_COLOR_TEMP]
        except KeyError:
            got_some_value += 1

        try:
            self.color.current = state_dict[GOVEE_KEY_COLOR]
        except KeyError:
            got_some_value += 1

        if got_some_value > 1:
            raise InvalidState("Either color or temperature must be provided.")

        # By this point we've made the update if possible


    #
    # Now this is the extra helper stuff
    #

    def _set_static_property(self, value):
        # This needs to be used as a safeguard to ensure the property is only set when the device is instantiated.
        raise NotImplementedError()

    def _set_state_property(self, value):
        # This is here as a complement to _set_static_property
        raise NotImplementedError()

class DeviceException(Exception):
    """
    This is the base class for any device exceptions.
    """

class InvalidState(DeviceException):
    """
    This class is used to indicate that there is some issue when setting the state of a device.
    """
