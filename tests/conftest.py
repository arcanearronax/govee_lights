"""
tests.conftest
"""
from src.goveelights.consts import (
    KEY_DEVICE,
    KEY_DEVICES,
    KEY_MODEL,
    KEY_DEVICE_NAME,
    KEY_CONTROL,
    KEY_RETRIEVE,
    KEY_SUPPORTED_COMMANDS,
    SUPPORTED_COMMANDS,
    KEY_PROPERTIES,
    KEY_COLOR_TEMP,
    KEY_RANGE,
    KEY_RANGE_MIN,
    KEY_RANGE_MAX,
    ATTR_ID,
    ATTR_MODEL,
    ATTR_DEVICE_NAME,
    ATTR_CONTROL,
    ATTR_RETRIEVE,
    ATTR_SUPPORTED_COMMANDS,
    ATTR_COLOR_TEMP_RANGE,
)
from src.goveelights.device import (
    DEVICE_MODES
)

from .account import (
    API_KEY,
    TEST_DEVICE_ID,
)

API_KEY_GOOD = API_KEY
API_KEY_BAD = "380d2e69-6ab1-0c21-e41d-07a5d4d41111"
API_KEY_INVALID = "80d2e69-6ab1-0c21-e41d-07a5d4d41111"
API_KEY_NONE = ""

DEVICE_ID_VALID = "12:34:56:78:90:ab:cd:ee"
DEVICE_ID_BAD = "z2:34:56:7z:z0:ab:cd:ez"
DEVICE_ID_INVALID = "12:34:56:78:90:ab:cd"
DEVICE_ID_NONE = ""
DEVICE_ID_GOOD = TEST_DEVICE_ID

DEVICE_MODEL_GOOD = "H6160"
DEVICE_NAME_GOOD = "Test Device"
DEVICE_CONTROL_GOOD = True
DEVICE_RETRIEVE_GOOD = True
TEMP_RANGE_MIN_GOOD = 3000
TEMP_RANGE_MAX_GOOD = 12000


def drop_key(data_dict, key):
    """
    This is used to return a new copy of a dict without the specified key.
    """
    return {k: v for k, v in data_dict.items() if k != key}


DEVICE_DATA_GOOD = {
    ATTR_ID: DEVICE_ID_VALID,
    ATTR_MODEL: DEVICE_MODEL_GOOD,
    ATTR_DEVICE_NAME: DEVICE_NAME_GOOD,
    ATTR_CONTROL: DEVICE_CONTROL_GOOD,
    ATTR_RETRIEVE: DEVICE_RETRIEVE_GOOD,
    ATTR_SUPPORTED_COMMANDS: SUPPORTED_COMMANDS,
    ATTR_COLOR_TEMP_RANGE: (TEMP_RANGE_MIN_GOOD, TEMP_RANGE_MAX_GOOD),
}

DEVICE_DATA_NO_DEVICE = drop_key(DEVICE_DATA_GOOD, KEY_DEVICE)
DEVICE_DATA_NO_MODEL = drop_key(DEVICE_DATA_GOOD, KEY_MODEL)
DEVICE_DATA_NO_DEVICE_NAME = drop_key(DEVICE_DATA_GOOD, KEY_DEVICE_NAME)
DEVICE_DATA_NO_CONTROL = drop_key(DEVICE_DATA_GOOD, KEY_CONTROL)
DEVICE_DATA_NO_RETRIEVE = drop_key(DEVICE_DATA_GOOD, KEY_RETRIEVE)
DEVICE_DATA_NO_SUPPORTED_COMMANDS = drop_key(
    DEVICE_DATA_GOOD, KEY_SUPPORTED_COMMANDS)
DEVICE_DATA_NO_PROPERTIES = drop_key(DEVICE_DATA_GOOD, KEY_PROPERTIES)

ALLOWED_MODES_ALL = DEVICE_MODES
ALLOWED_MODES_SOME = DEVICE_MODES[:-1]
ALLOWED_MODES_BAD = ALLOWED_MODES_SOME + ['bad_value']
ALLOWED_MODES_NONE = []
