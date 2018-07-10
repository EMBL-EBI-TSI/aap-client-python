"""
Classes and functions that encode, decode and verify JWT tokens

Encoded means encoded using base64, decoded tokens are json files
"""
from jwt import decode, MissingRequiredClaimError

from aap_client.public_keys import load_from_pem, load_from_der


_DEFAULT_CLAIMS = {u'iat', u'exp', u'sub', u'email', u'name', u'nickname'}


class TokenDecoder(object):  # pylint: disable=too-few-public-methods
    """
    Decodes and verifies tokens using an x509 certificate and checking
    always the same claims.
    """
    def __init__(self, filename, required_claims=None):
        """
        Args:
            filename: relative path to the file that contains the
                x509 certificate.
            required_claims: list of string with the claims that need to be
                present in the tokens.
        """
        if required_claims is None:
            required_claims = []

        self._required_claims = required_claims

        try:
            key = load_from_pem(filename)
        except ValueError:
            key = load_from_der(filename)

        self._key = key

    def decode(self, serialized_token):
        """ Decodes and verifies a token using a determined audience"""
        return verify_token(serialized_token, self._key,
                            required_claims=self._required_claims)


def verify_token(serialized_token, public_key,
                 required_claims=None):
    """
    Decodes and verifies a token given a certificate, the obligatory
    claims and a determined audience.
    """
    if required_claims is None:
        required_claims = []

    required_claims = set(required_claims).union(_DEFAULT_CLAIMS)
    payload = decode(serialized_token, public_key,
                     algorithms=[u'RS256'])
    for claim in required_claims:
        if payload.get(claim) is None:
            raise MissingRequiredClaimError(claim)

    return payload
