import jwt

from crypto_files import load_public_from_x509

class TokenDecoder:
    def __init__(self, filename, required_claims=[]):
        default_claims = {'iat', 'exp', 'sub', 'email', 'name', 'nickname'}
        self._required_claims = set(required_claims).union(default_claims)

        self._key = load_public_from_x509(filename)

    def decode(self, serialized_token, audience=None):
        return jwt.decode(serialized_token,
                          self._key,
                          audience=audience,
                          options={'require': self._required_claims})
