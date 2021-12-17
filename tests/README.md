# govee_lights/tests

This document details the different tests and purposes they serve.

# Tags

# Tests

## test_client.py

This file contains tests that validate a client object functions as its own
entity.

### TestCreate

This class handles validating that GoveeClient objects are created properly and
will throw errors when appropriate.

* Completed Tests
  * key_good
  * key_bad
  * key_invalid
  * key_none

### TestHeaders

This class is used to validate headers associated with a client object appear
and function as expected.

* Completed Tests
  * headers

### TestParameters

This class is used to validate parameters associated with a client object appear
and function as expected.

* Completed Tests
  * parameters

### TestGetRequests

This class is used to validate that a client object is able to submit the GET
requests the Govee API supports.

* Completed Tests
  * power_on
  * get_device_state

### TestPutRequests

This class is used to validate that a client object is able to submit the PUT
requests the Govee API supports.

* Completed Tests
  * cmd_power_off
  * cmd_power_on
  * brightness_max
  * brightness_min
  * color_rgb_red
  * color_rgb_green
  * color_rgb_blue
  * color_temp_max
  * color_temp_min


## test_devices.py

This file contains tests that validate a device functions as its own entity.

### TestCreateDeviceHub

This class contains tests related to the creation of a device when a hub is
provided.

* Completed Tests
  * create_with_hub_only

### TestCreateDeviceID

This class contains tests that validate the creation of a device when a device
id is provided.

* Completed Tests
  * device_id_valid
  * device_id_invalid
  * device_id_bad
  * device_id_good

### TestCreateDeviceDict

This class contains tests that validate the creation of a device when a device
dict is provided.

* Completed Tests
  * device_dict_valid

* Incomplete Tests
  * device_dict_invalid
  * device_dict_bad

### TestProperties

This class contains tests related to the properties of a device.

* Completed Tests
  * power_cycle
  * online_cycle
  * allowed_modes_cycle
  * registered_hub
  * registered_no_hub

### TestUninitialedDevice

This class contains tests related to devices in an uninitialized status.

* Completed Tests
  * power_cycle
  * brightness_cycle
  * color_rgb_cycle
  * color_temp_cycle

### TestInitializedDevice

This class contains tests related to devices in an initialized status.

* Completed Tests
  * power_cycle
  * brightness_cycle
  * color_rgb_cycle
  * color_temp_cycle

## test_hub.py

This file contains tests that validate a bug functions as its own entity.

### TestCreateHub

This class contains tests related to devices in an initialized status.

* Completed Tests

* WIP Tests
  * create_client_good
  * create_client_invalid
  * create_client_none

### TestDeviceRegistration

This class contains tests related to registering a device with a hub.

* Completed Tests

* WIP Tests

### TestDeviceManagement

This class contains tests related to the management of registered devices.

* Completed Tests
  * build_devices

* WIP Tests

## Auxiliary Files

These files do not contain tests themselves, but contain supporting data.

### account.py

The account file contains values which are unique to the user's Govee account.
The contents of this file should not be made available to other users.

### conftest.py

This file contains static data which should not need to be modified or added to
unless tests are being changed.
