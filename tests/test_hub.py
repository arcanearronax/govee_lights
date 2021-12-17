import unittest

from src.goveelights.client import (
    GoveeClient,
    HEADER_API_KEY,
    KEY_DEVICES,
    )
from src.goveelights.exceptions import (
    GoveeHubException
)
from src.goveelights.hub import GoveeHub

from .conftest import API_KEY_GOOD


class TestCreateHub(unittest.TestCase):
    """
    This is used to manage hub creation tests.
    """

    def setUp(self):
        """
        This is used to setup the tests.
        """
        self.client = GoveeClient(API_KEY_GOOD)

    def tearDown(self):
        """
        This is used to clean up after the tests.
        """

    def test_hub_create_client_good(self):
        """
        This is used to validate a hub can be created.
        """
        hub = GoveeHub(self.client)
        self.assertIs(self.client, hub.client,
                      "Failed to successfully set client")

    def test_hub_create_client_invalid(self):
        """
        This is used to validate a hub can be created.
        """
        client = ""
        with self.assertRaises(GoveeHubException):
            GoveeHub(client)

    def test_hub_create_client_none(self):
        """
        This is used to validate a hub can be created.
        """
        client = None
        with self.assertRaises(GoveeHubException):
            GoveeHub(client)


class TestDeviceRegistration(unittest.TestCase):
    """
    This is used to validate the device registration process.
    """


class TestDeviceManagement(unittest.TestCase):
    """
    This is used to validate that the hub can manage devices.
    """

    @classmethod
    def setUpClass(cls):
        """
        This is used to setup the class for tests.
        """

    def setUp(self):
        """
        This is used to setup the tests.
        """
        client = GoveeClient(API_KEY_GOOD)
        self.hub = GoveeHub(client)

    def tearDown(self):
        """
        This is used to clean up after the tests.
        """

    def test_build_devices(self):
        """
        This is used to validate the client can be accessed.
        """
        self.hub.build_devices()
        self.assertTrue(hasattr(self.hub, KEY_DEVICES))
