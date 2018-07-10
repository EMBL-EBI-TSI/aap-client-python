"""Utilities to retrieve private an public keys from files"""
from cryptography.x509 import load_pem_x509_certificate as load_pem
from cryptography.x509 import load_der_x509_certificate as load_der
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


def load_public_from_pem(pem_filename):
    """Opens an X509 certificate in PEM format and returns its public key"""
    with open(pem_filename, 'r') as cert_file:
        cert = load_pem(cert_file.read().encode(),
                        default_backend())
        key = cert.public_key()
    return key

def load_public_from_der(der_filename):
    """Opens an X509 certificate in DER format and returns its public key"""
    with open(der_filename, 'rb') as cert_file:
        cert = load_der(cert_file.read(),
                        default_backend())
        key = cert.public_key()
    return key


def _load_private_from_pem(pem_filename, secret=None):
    """Opens a PEM and returns its private key with a secret"""
    with open(pem_filename, 'rb') as pem_file:
        private_key = load_pem_private_key(
            pem_file.read(),
            password=secret,
            backend=default_backend())
    return private_key
