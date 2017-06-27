from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

import jwt


class TokenEncoder:
    def __init__(self, key_filename, secret=None):
        with open(key_filename, 'rb') as key_file:
             self._private_key = load_pem_private_key(
                 key_file.read(),
                 password=secret,
                 backend=default_backend())

    def encode(self, claims):
        return jwt.encode(claims, self._private_key, algorithm='RS256')
