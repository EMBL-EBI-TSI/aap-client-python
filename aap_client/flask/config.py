"""Exports the configuration for managing tokens within flask"""
from flask import current_app


class _Config(object):  # pylint: disable=too-few-public-methods
    """
    Helper object to help verify and retrieve configuration options for the
    AAP's Flask extension.

    Having this class separate in its on module ensures the configurations
    options are loaded when the Flask application gets run, and not when the
    JWT Client gets instatiated.

    This means that changing the configuration can be done through
    ``app.config`` after instatiating ``JWTClient`` and before running the
    Flask app.
    """
    @property
    def public_key(self):
        """
        Method that retrieves the public key used by the flask application
        """
        key = current_app.config[u'JWT_PUBLIC_KEY']
        if not key:
            raise RuntimeError(u'JWT_PUBLIC_KEY needs to be added to '
                               u'the Flask app\'s config in order to '
                               u'process tokens from the AAP.')
        return key


CONFIG = _Config()
