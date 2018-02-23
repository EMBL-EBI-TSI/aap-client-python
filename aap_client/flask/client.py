"""
Entry point needed to enable the decorators and the configuration
for managing tokens in a Flask environment
"""
from flask import jsonify

from aap_client.flask.exceptions import FlaskException


class JWTClient(object):  # pylint: disable=too-few-public-methods
    """
    This class needs to be instatiated right after the Flask server is

    Usage:
        web_app = Flask(__name__)
        JWTClient(web_app)
    """
    def __init__(self, app=None):
        """
        :param app: a Flask application
        """
        if app is not None:
            app.jwt_client = self

            app.config.setdefault(u'PROPAGATE_EXCEPTIONS', True)
            app.config.setdefault(u'JWT_PUBLIC_KEY', None)

            @app.errorhandler(FlaskException)
            def handle_invalid_usage(error):  # pylint: disable=W0612,C0111
                response = jsonify(error.to_dict())
                response.status_code = error.status_code
                return response
