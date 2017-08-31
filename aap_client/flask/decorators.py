from future.utils import raise_with_traceback

from functools import wraps

from jwt import DecodeError, InvalidTokenError

from aap_client.tokens import decode_token
from aap_client.flask.config import config
from aap_client.flask.exceptions import (
    FlaskException, AuthenticationFailed, NotAuthenticated, ParseError
)

from flask import current_app, request

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:
    from flask import _request_ctx_stack as ctx_stack


def jwt_required(func):
    """
    Decorator that ensures that the request contains a valid token.
    Used to ensure the request to a view is from an authorized user.

    :param func: The decorated view function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _load_jwt_to_context()
        return func(*args, **kwargs)
    return wrapper


def jwt_optional(func):
    """
    Decorator that changes the flask context if the request contains
    a valid token.
    Used to retrieve the authorized user if the token is valid.

    :param func: The decorated view function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            _load_jwt_to_context()
        except FlaskException:
            pass
        return func(*args, **kwargs)
    return wrapper


def get_user():
    """
    Returns the user in the current context / request, otherwise returns None
    """
    return getattr(ctx_stack.top, u'user', None)


def _load_jwt_to_context():
    claims = _decode_from_request()
    ctx_stack.top.token = claims
    ctx_stack.top.user = claims[u'sub']


def _decode_from_request():
    # verify that the auth header exists
    auth_header = request.headers.get(u'Authorization', None)
    if not auth_header:
        raise NotAuthenticated(u'Request is missing the Authorization header')
    # verify that the header is in the correct format
    # Authorization: Bearer <JWT>
    splitted_header = auth_header.split()
    if len(splitted_header) != 2 and splitted_header[0] == u'Bearer:':
        raise ParseError(u'Invalid Authorization header, \
                           expected \'Bearer <JWT>\'')

    jwt = splitted_header[1]

    try:
        return decode_token(jwt, config.public_key)
    except DecodeError as e:
        raise_with_traceback(
            ParseError(u'Unable to decode token: {}'.format(e)))
    except InvalidTokenError:
        raise_with_traceback(
            AuthenticationFailed(message=u'Request contains an invalid token'))


def _get_jwt_client():
    try:
        return current_app.jwt_client
    except AttributeError:
        raise RuntimeError(u'JWTClient must be initialized with a flask '
                           u'application before using this method')
