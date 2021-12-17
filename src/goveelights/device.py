"""
goveelights.device

This is the base class for Govee devices that use the API.

"""
import re
import logging
<<<<<<< HEAD

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

=======
import logging.config

from .color import (
    Color,
    validate_temp_range,
)
from .consts import (
    POWER_STATES,
    SUPPORTED_MODELS,
    SUPPORTED_COMMANDS,
    ATTR_POWER_STATE,
    ATTR_BRIGHTNESS,
    ATTR_COLOR,
    ATTR_COLOR_TEMP,
    BRIGHTNESS_MAX,
    BRIGHTNESS_MIN,
    ONLINE_STATES,
    ATTR_DEVICE_NAME,
    ATTR_ID,
)
from .exceptions import (
    DeviceException,
    InvalidState,
    InvalidValue,
)
from .settings import LOGGING

MODE_TEMP = "temp"
MODE_COLOR = "color"
DEVICE_MODES = [MODE_TEMP, MODE_COLOR]
REGEX_DEVICE_ID = "^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){7}$"

ALLOWED_MODES = (MODE_TEMP, MODE_COLOR)

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


def validate_device_id(value):
    """
    This is used to validate that the device_id meets the Govee format.
    If it does, device_id is returned, None otherwise.
    """
    try:
        value_str = str(value)
    except Exception as e:
        raise InvalidValue("Cannot process Device ID") from e
    else:
        if re.match(REGEX_DEVICE_ID, value_str):
            return value_str
        else:
            raise InvalidValue("Device ID is not acceptable")
    raise InvalidValue("Invalid Device Id")


def validate_power_state(value):
    """
    This is used to validate device power states.
    """
    if value in POWER_STATES:
        return value

    raise InvalidValue("Power state is not valid")


def validate_brightness(value):
    """
    This is used to validate the brightness is an int between 1 and 100.
    """
    try:
        value_int = int(value)
    except ValueError as ve:
        raise InvalidValue("Brightness is not an int") from ve
    except Exception as e:
        raise InvalidValue("Cannot process Brightness") from e
    else:
        if BRIGHTNESS_MIN <= value_int <= BRIGHTNESS_MAX:
            return value_int
        else:
            raise InvalidValue("Brightness is not acceptable")

    raise InvalidValue("Invalid Brightness")


def validate_color(color):
    """
    This is used to validate color values are correct
    """
    if type(color) is dict:
        color = Color(rgb_dict=color)
    elif type(color) is not Color:
        raise InvalidValue("Invalid type for color.")

    return color


def validate_color_temp(value, min=0, max=0):
    """
    This is used to validate a provided Color Temp is within the specified
    range.
    """
    if not type(value) is int and type(min) is int and type(max) is int:
        raise InvalidValue("Provided values are not ints")

    if min:
        if max and max < min:
            raise InvalidValue("Value is not within Color Temp Range")
        if value < min:
            raise InvalidValue("Value is not within Color Temp Range")
    if max:
        if value > max:
            raise InvalidValue("Value is not within Color Temp Range")

    return value


class GoveeDevice():
    """
    This is the base class for an API compatible Govee device.
    This is the digital representation of the physical device.
    """

    attr_validator = {
        ATTR_POWER_STATE: validate_power_state,
        ATTR_BRIGHTNESS: validate_brightness,
        ATTR_COLOR: validate_color,
        ATTR_COLOR_TEMP: validate_color_temp,
    }

    def __init__(self, hub=None, device_id=None, device_dict=None, initialized=True):
        """
        The user may create an instance by providing a device ID or a dict
        containing the device info, provided by Govee.
        """
        logger.info(f"Creating device {device_id} - ")

        # Need to make sure this exists
        self._color_temp_range = (None, None)

        # Manually create a device
        if device_id:
            try:
                self.id = device_id
                if hub:
                    hub.register_device(self)
            except Exception as e:
                raise DeviceException(
                    "Failed to set device ID") from e

        # Create a device from Govee data
        elif device_dict:
            for key, value in device_dict.items():
                logger.debug(f"Attempting to set {key}={value}")
                try:
                    setattr(self, key, value)
                except Exception as e:
                    raise DeviceException("Unknown Error") from e
                else:
                    logger.debug("Success")

        # Make sure we set the device_id
            try:
                device_id = self.id
                if hub:
                    hub.register_device(self)
            except Exception as e:
                raise InvalidState(
                    "Failed to find Device ID") from e
        else:
            raise DeviceException("Insufficient data to create device")

        self.initialized = initialized
        logger.debug("Device build successful")

    def __repr__(self):
        try:
            if hasattr(self, ATTR_DEVICE_NAME):
                return str(self.device_name)
            elif hasattr(self, ATTR_ID):
                return str(self.id)
            return "Unconfigured Device"
        except AttributeError:
            return "Broken Device"
        except Exception as e:
            raise DeviceException("Failed to generate representation") from e

    # Decorator used to facilitate API requesting updates
    def api_update(attr):
        def wrapper(func):
            def initialize_check_and_update(*args, **kwargs):
                # We're only going to use this for instance methods
                device = args[0]
                # This is just here as a hot fix.
                if attr == ATTR_COLOR_TEMP:
                    value = type(device).attr_validator[attr](
                        args[1],
                        device.color_temp_range[0],
                        device.color_temp_range[1]
                    )
                else:
                    value = type(device).attr_validator[attr](args[1])
                args = (args[0],) + (value,) + args[2:]
                try:
                    if device.initialized:
                        if attr == ATTR_COLOR:
                            if not device.hub.control_device(
                                device,
                                attr,
                                value.rgb_dict()
                            ):
                                return None
                        else:
                            if not device.hub.control_device(
                                device,
                                attr,
                                value
                            ):
                                return None

                    return func(*args, **kwargs)
                except AttributeError as ae:
                    raise DeviceException("Device does not have a hub") from ae

            return initialize_check_and_update
        return wrapper
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    #
    # These are Govee device properties
    #

    @property
<<<<<<< HEAD
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
=======
    def hub(self):
        """
        This is used to provide access to the hub a device is registered with.
        """
        try:
            return self._hub
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve hub") from e

    @property
    def id(self):
        """
        This is the unique ID used to identify the device. Govee identifies it
        as the MAC address, but it has 8 octets.
        """
        try:
            return self._device_id
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve ID") from e

    @id.setter
    def id(self, device_id):
        """
        Set the Device ID iff it's not set.
        """
        try:
            self._device_id = validate_device_id(device_id)
        except Exception as e:
            raise DeviceException("Failed to set ID") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def model(self):
        try:
            return self._model
        except AttributeError:
            return None
<<<<<<< HEAD

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
=======
        except Exception as e:
            raise DeviceException("Failed to retrieve Model") from e

    @model.setter
    def model(self, model_name):
        try:
            if model_name not in SUPPORTED_MODELS:
                raise DeviceException("Invalide model provided")
            self._model = model_name
        except Exception as e:
            raise DeviceException("Failed to set Model") from e

    @property
    def device_name(self):
        try:
            return self._device_name
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Device Name") from e

    @device_name.setter
    def device_name(self, device_name):
        try:
            self._device_name = device_name
        except Exception as e:
            raise DeviceException("Failed to retrieve Device Name") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def controllable(self):
        try:
            return self._controllable
        except AttributeError:
            return None
<<<<<<< HEAD

    @controllable.setter
    def controllable(self, is_controllable=True):
        try:
            self._controllable = bool(is_controllable)
        except Exception:
            self._controllable = False
=======
        except Exception as e:
            raise DeviceException("Failed to retrieve Controllable") from e

    @controllable.setter
    def controllable(self, is_controllable=False):
        try:
            self._controllable = bool(is_controllable)
        except Exception as e:
            raise DeviceException("Failed to set Controllable") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def retrievable(self):
        try:
            return self._retrievable
        except AttributeError:
            return None
<<<<<<< HEAD
=======
        except Exception as e:
            raise DeviceException("Failed to retrieve Retrievable") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @retrievable.setter
    def retrievable(self, is_retrievable=True):
        try:
            self._retrievable = bool(is_retrievable)
<<<<<<< HEAD
        except Exception:
            self._retrievable = False

    @property
    def supported_commands(self):
        return self._supported_commands
=======
        except Exception as e:
            raise DeviceException("Failed to set Retrievable") from e

    @property
    def supported_commands(self):
        try:
            return self._supported_commands
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve Supported Commands") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @supported_commands.setter
    def supported_commands(self, command_iterable):
        """
        This is responsible for reading in supported commands for an iterable.
        """
<<<<<<< HEAD
        logger.info(f"Command iterable: {command_iterable}")
        self._supported_commands = [
            x for
            x in command_iterable
            if x in GOVEE_SUPPORTED_COMMANDS
        ]
=======
        try:
            self._supported_commands = [
                x for
                x in command_iterable
                if x in SUPPORTED_COMMANDS
            ]
        except Exception as e:
            raise DeviceException("Failed to set Suppoerted Commands") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def color_temp_range(self):
        """
        The permitted range of color temperatures
        """
<<<<<<< HEAD
        return self._color_temp_range
=======
        try:
            return self._color_temp_range
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Temp Range") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @color_temp_range.setter
    def color_temp_range(self, range_tuple):
        """
        The permitted range of color temperatures
        """
<<<<<<< HEAD

        for i in range_tuple:
            assert i >= 0, f"Invalid temperature in range - {i}"

        assert range_tuple[0] <= range_tuple[1], f"Invalid temperature range"

        self._color_temp_range = range_tuple
=======
        logger.debug(f"color_temp_range: {range_tuple}")
        try:
            # self._color_temp_range = validate_temp_range(range_tuple)
            self._color_temp_range = range_tuple
        except Exception as e:
            raise DeviceException("Failed to set Color Temp Range") from e

    @property
    def allowed_modes(self):
        try:
            return self._allowed_modes
        except AttributeError:
            return []
        except Exception as e:
            raise DeviceException("Failed to retrieve Allowed Modes") from e

    @allowed_modes.setter
    def allowed_modes(self, modes):
        if not all(mode in DEVICE_MODES for mode in modes):
            raise InvalidValue("Invalid device mode identified.")
        try:
            self._allowed_modes = modes
        except Exception as e:
            raise DeviceException("Failed to set Allowed Modes") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    #
    # Device state information below here
    #

    @property
    def online(self):
<<<<<<< HEAD
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
=======
        """
        This is used to safely retrieve the online attribute of the device.
        """
        try:
            return self._online
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Online") from e

    @online.setter
    def online(self, is_online):
        # assert self.retrievable, "Online status is not retrievable."
        try:
            if bool(is_online) in ONLINE_STATES:
                self._online = is_online
            else:
                raise DeviceException("Online State is invalid")
        except Exception as e:
            raise DeviceException("Failed to set Online") from e

    @property
    def registered(self):
        """
        This is just a simple check to make sure the device is registered.
        """
        try:
            if self.hub:
                return True
            else:
                return False
        except AttributeError:
            return False
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve Registration Flag") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def power_state(self):
        try:
            return self._power_state
<<<<<<< HEAD
        except AttributeError:
            return GOVEE_POWER_OFF

    @power_state.setter
    def power_state(self, power_state):
        self._power_state = power_state
=======
        # Warn that the attribute does not exist
        except AttributeError:
            return None
        # Raise a DeviceException if anything else happens
        except Exception as e:
            raise DeviceException(
                "Failed to retrieve power state") from e

    @power_state.setter
    @api_update(ATTR_POWER_STATE)
    def power_state(self, power_state):
        """
        This is used to set the power state for a device.
        It raises an AssertionError if the power state provided is invalid.
        It raises a DeviceException if any other Exception is raised.
        """
        try:
            self._power_state = power_state
        except Exception as e:
            raise DeviceException("Failed to set Power State") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7

    @property
    def brightness(self):
        try:
            return self._brightness
<<<<<<< HEAD
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
=======
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve brightness") from e

    @brightness.setter
    @api_update(ATTR_BRIGHTNESS)
    def brightness(self, brightness):
        """
        This is used to update the brightness of the device if the hub is able
        to handle the request.
        """
        try:
            self._brightness = brightness
        except Exception as e:
            raise DeviceException("Failed to set Brightness") from e

    @property
    def color_mode(self):
        try:
            return self._color_mode
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Mode") from e

    @color_mode.setter
    def color_mode(self, mode):
        """
        This is used to set the current color mode of a device.
        """
        try:
            #if mode not in self.allowed_modes:
            #    raise InvalidState("Mode is not permitted")
            self._color_mode = mode
        except Exception as e:
            raise DeviceException("Failed to set Color Mode") from e

    @property
    def color(self):
        """
        This is used to retrieve the color of a device.
        """
        try:
            if self.color_mode == MODE_COLOR:
                return self._color
            else:
                return None
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color") from e

    @color.setter
    @api_update(ATTR_COLOR)
    def color(self, color):
        """
        This is used to handle setting the color of a device.
        """
        try:
            self._color = color
            self.color_mode = MODE_COLOR
        except Exception as e:
            raise DeviceException("Failed to set Color") from e

    @property
    def color_temp(self):
        """
        This is used to retrieve the device's color temp value, if in color
        temp mode.
        If the device is not in color temp mode, it raises an error.
        """
        try:
            if self.color_mode == MODE_TEMP:
                return self._color_temp
            else:
                return None
        except AttributeError:
            return None
        except Exception as e:
            raise DeviceException("Failed to retrieve Color Temp") from e

    @color_temp.setter
    @api_update(ATTR_COLOR_TEMP)
    def color_temp(self, color_temp):
        """
        This is used to handle setting the color temp of a device.
        """
        try:
            self._color_temp = color_temp
            self.color_mode = MODE_TEMP
        except Exception as e:
            raise DeviceException(
                "Failed to set Color Temp") from e

    @property
    def initialized(self):
        """
        This is used to indicate whether a device has been initialized and
        therefore communicates with the client.
        """
        try:
            return self._initialized
        except AttributeError:
            return False

    @initialized.setter
    def initialized(self, init_status):
        """
        This is used to control whether a device has been initialized.
        """
        try:
            self._initialized = bool(init_status)
        except ValueError:
            raise DeviceException("Status must be boolean")

    #
    # This is used for any communication with the hub.
    #

    def refresh(self):
        """
        This is called to refresh device data.
        The method relies on calling the hub to update the device itself.
        """
        logger.info("Refreshing device...")
        try:
            self.hub.refresh_device(self.id)
        except Exception as e:
            raise DeviceException("Unable to refresh device") from e
>>>>>>> 95206d1969f7285686979b827c82104c492977d7
