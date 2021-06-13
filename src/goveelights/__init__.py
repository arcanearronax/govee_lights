"""

goveelights.__init__

This contains information shared throughout the package.

"""

from .client import GoveeClient

from .device import (
    GoveeDevice,
    DeviceException,
    InvalidState,
)

from .hub import (
    GoveeHub,
    GOVEE_BRIGHTNESS_MIN,
    GOVEE_BRIGHTNESS_MAX,
    GOVEE_COLOR_MIN,
    GOVEE_COLOR_MAX,
    GOVEE_POWER_ON,
    GOVEE_POWER_OFF,
)

import logging
logging.basicConfig(filename='testing.log', level=logging.INFO)
