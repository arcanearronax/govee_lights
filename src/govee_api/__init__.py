"""

govee_api.__init__

This contains information shared throughout the package.

"""

from .client import GoveeClient


from .device import (
    GoveeDevice,
    GOVEE_SUPPORTED_MODELS,
    DeviceException,
    InvalidState
)


from .hub import (
    GoveeHub,
    GOVEE_BRIGHTNESS_MIN,
    GOVEE_BRIGHTNESS_MAX,
    GOVEE_COLOR_MIN,
    GOVEE_COLOR_MAX
)

import logging

#logger = logging.getLogger(__name__)
logging.basicConfig(filename='testing.log', level=logging.INFO)

GOVEE_CMD_TURN = "turn"
GOVEE_CMD_BRIGHT = "brightness"
GOVEE_CMD_COLOR = "color"
GOVEE_CMD_COLORTEM = "colorTem"
GOVEE_SUPPORTED_COMMANDS = [
    GOVEE_CMD_TURN, GOVEE_CMD_BRIGHT, GOVEE_CMD_COLOR, GOVEE_CMD_COLORTEM
]

#GOVEE_HUB = GoveeHub()
