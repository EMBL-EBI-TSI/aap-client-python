class FlaskException(Exception):
    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class AuthenticationFailed(FlaskException):
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class NotAuthenticated(FlaskException):
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class ParseError(FlaskException):
    def __init__(self, message, status_code=400, payload=None):
        FlaskException.__init__(self, message, status_code, payload)
