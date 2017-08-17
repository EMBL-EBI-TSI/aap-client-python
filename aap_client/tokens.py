import jwt

from aap_client.crypto_files import load_public_from_x509, load_private_from_pem


_DEFAULT_CLAIMS = {'iat', 'exp', 'sub', 'email', 'name', 'nickname'}


class TokenDecoder:
    def __init__(self, filename, required_claims=[]):
        self._required_claims = required_claims
        self._key = load_public_from_x509(filename)

    def decode(self, serialized_token, audience=None):
        return decode_token(serialized_token, self._key,
                            required_claims=self._required_claims,
                            audience=audience)


class TokenEncoder:
    def __init__(self, key_filename, secret=None):
        self._private_key = load_private_from_pem(key_filename, secret)

    def encode(self, claims):
        return encode_token(claims, self._private_key)


# Functions that can be used when an object to store the keys cannot be

def decode_token(serialized_token, public_key,
                 required_claims=[], audience=None):
    required_claims = set(required_claims).union(_DEFAULT_CLAIMS)
    return jwt.decode(serialized_token, public_key,
                      audience=audience, options={'require': required_claims})


def encode_token(claims, private_key):
        return jwt.encode(claims, private_key, algorithm='RS256')
