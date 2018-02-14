class FlaskException(Exception):
    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        r_v = dict(self.payload or ())
        r_v[u'message'] = self.message
        return r_v


class AuthenticationFailed(FlaskException):
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class NotAuthenticated(FlaskException):
    def __init__(self, message, status_code=401, payload=None):
        FlaskException.__init__(self, message, status_code, payload)


class ParseError(FlaskException):
    def __init__(self, message, status_code=400, payload=None):
        FlaskException.__init__(self, message, status_code, payload)
