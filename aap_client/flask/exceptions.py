"""
Exceptions thrown by the rest of the package
"""


class FlaskException(Exception):
    """
    This class enhances exceptions so they can be easily serialized
    and be show by the web app as they choose (JSON, for example)
    """
    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        This method is the one that permits exception messages to be handled
        gracefully.
        """
        r_v = dict(self.payload or ())
        r_v[u'message'] = self.message
        return r_v


class AuthenticationFailed(FlaskException):  # pylint: disable=C0111
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class NotAuthenticated(FlaskException):  # pylint: disable=C0111
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class ParseError(FlaskException):  # pylint: disable=C0111
    def __init__(self, message, status_code=400, payload=None):
        FlaskException.__init__(self, message, status_code, payload)
