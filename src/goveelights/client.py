"""

goveelights.client

This contains the base class for all Govee devices.

"""
from uuid import UUID
import requests
import json

import logging

GOVEE_HEADER_CONT_TYPE = "application/json"
GOVEE_HEADER_API_KEY = "Govee-API-Key"

GOVEE_QUERY_DEVICE = "device"
GOVEE_QUERY_MODEL = "model"

GOVEE_DATA_DICT_KEY = "data"
GOVEE_UUID_VERSION = 4

SUCCESS_CODES = [200, 201, 202]

logger = logging.getLogger(__name__)
#logging.basicConfig(filename='testing.log', level=logging.INFO)

class GoveeClient():
    """
    This is the base class for the Govee API hub.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    #
    # Stuff the user would need to call
    #

    @property
    def api_key(self):
        return self._api_key

    # May not actually need this...
    @api_key.setter
    def api_key(self, api_key):
        self._api_key = GoveeClient._validate_uuid(api_key)

    #
    # Here contains methods sending data TO the API
    #

    def get_data(self, req_uri, device_id=None, model=None):
        """
        This is used to by the hub to submit data requests to the Govee API. It returns a dict with information from the API.
        """
        # Need to validate the parameters
        try:
            req = requests.get(
                req_uri,
                headers=self._generate_headers(),
                params=GoveeClient._generate_params(device_id, model)
            )
        except Exception as e:
            logger.error(f"GET error: {e}")
            return None

        else:
            logger.info(f"Got status code: {req.status_code}")
            if req.status_code not in SUCCESS_CODES:
                raise InvalidResponse(f"Received a {req.status_code} response.")

            ret_dict = json.loads(req.text)[GOVEE_DATA_DICT_KEY]
            logger.info(f"get_data - {ret_dict}")
            return ret_dict

    def put_data(self, req_uri, device_id, model, req_body):
        """
        This is responsible for sending commands intended to control a specific light.
        """

        # This will require additional logic to handle valid and invalid commands

        try:
            req = requests.put(
                req_uri,
                headers=self._generate_headers(),
                params=GoveeClient._generate_params(device_id, model),
                json=req_body
            )
        except Exception as e:
            logger.error(f"put_data error - {e}")
            return None

    #
    # This is just the helper stuff
    #

    def _generate_headers(self):
        # Just throwing this here for now
        return {
            GOVEE_HEADER_API_KEY: self.api_key,
            "Content-Type": GOVEE_HEADER_CONT_TYPE,
        }

    def _generate_params(device_id=None, model=None):
        """
        This is used to generate the parameters used in some API requests.
        """
        logger.info(f"Generating params for {device_id} - {model}")
        if device_id and model:
            return {
                GOVEE_QUERY_DEVICE: device_id,
                GOVEE_QUERY_MODEL: model,
            }
        # In case we don't have parameters to generate
        return None

    def _validate_uuid(uuid_key):
        """
        This method receives a string and validates it's a UUIDv4 key. It returns the key as a string if it's valid, throws an error otherwise.
        """
        try:
            key_version = UUID(uuid_key).version
            logger.info(f"Got valid key version: {key_version}")
        except (ValueError, TypeError):
            logger.info(f"Invalid UUID key provided")
            raise InvalidAPIKey("Not a valid UUID.")
        else:
            if key_version != GOVEE_UUID_VERSION:
                raise InvalidAPIKey(f"UUID is not version {GOVEE_UUID_VERSION}")

        logger.info("Returning valid UUID key")
        return uuid_key

class GoveeException(Exception):
    """
    A Govee error occurred.
    """

class InvalidDevice(GoveeException):
    """
    An invalid device was present in the registry.
    """

class InvalidAPIKey(GoveeException):
    """
    An invalid Govee API key was provided.
    """

class InvalidResponse(GoveeException):
    """
    A non-200 code was received when submitting an API request.
    """
