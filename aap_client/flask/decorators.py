"""
Contains flask decorators and some helper functions
in order to integrate jwt tokens in flask in a natural way
"""
from functools import wraps

from future.utils import raise_with_traceback

from jwt import DecodeError, InvalidTokenError as JWTInvalidTokenError

from flask import current_app, request

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:
    from flask import _request_ctx_stack as ctx_stack

from aap_client.tokens import verify_token
from aap_client.flask.config import CONFIG
from aap_client.flask.exceptions import (
    InvalidRequestError,
    InvalidTokenError,
    NoAuthenticationError
)


def jwt_required(func):
    """
    Decorator that ensures that the request contains a valid token.
    Used to ensure the request to a view is from an authorized user.

    :param func: The decorated view function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):  # pylint: disable=C0111
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
    def wrapper(*args, **kwargs):  # pylint: disable=C0111
        try:
            _load_jwt_to_context()
        except NoAuthenticationError:
            pass
        except InvalidTokenError:
            pass
        return func(*args, **kwargs)
    return wrapper


def get_user():
    """
    Returns the user in the current context / request, otherwise returns None
    """
    return getattr(ctx_stack.top, u'user', None)


def get_claims():
    """
    Returns the claims in the current context / request, otherwise None
    """
    return getattr(ctx_stack.top, u'token', None)


def _load_jwt_to_context():
    claims = _decode_from_request()
    ctx_stack.top.token = claims
    ctx_stack.top.user = claims[u'sub']


def _decode_from_request():
    # verify that the auth header exists
    auth_header = request.headers.get(u'Authorization', None)
    if not auth_header:
        raise NoAuthenticationError(u'Authorization Required')
    # verify that the header is in the correct format
    # Authorization: Bearer <JWT>
    splitted_header = auth_header.split()
    if len(splitted_header) != 2 or not auth_header.startswith(u'Bearer '):
        raise InvalidRequestError(u'Invalid Authorization header, '
                                  u'expected \'Bearer <JWT>\'')

    jwt = splitted_header[1]

    try:
        return verify_token(jwt, CONFIG.public_key)
    except DecodeError as err:
        raise_with_traceback(
            InvalidTokenError(u'Unable to decode token: {}'.format(err)))
    except JWTInvalidTokenError as err:
        raise_with_traceback(
            InvalidTokenError(u'{}'.format(err)))


def _get_jwt_client():
    try:
        return current_app.jwt_client
    except AttributeError:
        raise RuntimeError(u'JWTClient must be initialized with a flask '
                           u'application before using this method')
