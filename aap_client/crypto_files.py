"""Utilities to retrieve private an public keys from files"""
from cryptography.x509 import load_pem_x509_certificate as load_pem
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


def load_public_from_x509(x509_filename):
    """Opens an X509 cert and returns its public key"""
    with open(x509_filename, 'r') as cert_file:
        cert = load_pem(cert_file.read().encode(),
                        default_backend())
        key = cert.public_key()
    return key


def load_private_from_pem(pem_filename, secret=None):
    """Opens a PEM and returns its private key with a secret"""
    with open(pem_filename, 'rb') as pem_file:
        private_key = load_pem_private_key(
            pem_file.read(),
            password=secret,
            backend=default_backend())
    return private_key
