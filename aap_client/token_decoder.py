from cryptography.x509 import load_pem_x509_certificate as load_pem
from cryptography.hazmat.backends import default_backend

import jwt


class TokenDecoder:
    def __init__(self, filename):
        with open(filename, 'r') as cert_file:
             cert = load_pem(cert_file.read(), default_backend())
             self._key = cert.public_key()

    def decode(self, serialized_token):
        return jwt.decode(serialized_token, self._key)
