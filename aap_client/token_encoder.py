import jwt

from crypto_files import load_private_from_pem

class TokenEncoder:
    def __init__(self, key_filename, secret=None):
        self._private_key = load_private_from_pem(key_filename, secret)

    def encode(self, claims):
        return jwt.encode(claims, self._private_key, algorithm='RS256')
