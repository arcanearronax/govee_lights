import unittest

from random import randint

class HexId():

    KEY_LENGTH_DEFAULT = 8 # Number of bytes for the ID length

    @staticmethod
    def generate_hex_value():
        """
        This is here to generate individual hex values
        """
        return str(hex(randint(0,15))[2:])

    @staticmethod
    def format_key(key_string, length=KEY_LENGTH_DEFAULT):
        """
        The user passes a string of hex characters and returns a string formatted with colons properly
        """

        ret_key = ':'.join(str(i:i+2) for i in )

    @staticmethod
    def valid_key(length=KEY_LENGTH_DEFAULT):
        """
        This is used to generate an appropriate length
        """


class TestGoveeDeviceId(unittest.TestCase):

    def _generate_valid

    @property
    def static_valid_id(self):
        """
        This is used to generate a static valid hex id.
        """

    def test_id_valid(self):
        """
        This generates a random 8-byte formatted hex string.
        """
