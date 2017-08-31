from flask import jsonify

from aap_client.flask.exceptions import FlaskException


class JWTClient(object):
    def __init__(self, app=None):
        """
        :param app: a Flask application
        """
        if app is not None:
            app.jwt_client = self

            app.config.setdefault('PROPAGATE_EXCEPTIONS', True)
            app.config.setdefault('JWT_PUBLIC_KEY', None)

            @app.errorhandler(FlaskException)
            def handle_invalid_usage(error):
                response = jsonify(error.to_dict())
                response.status_code = error.status_code
                return response
