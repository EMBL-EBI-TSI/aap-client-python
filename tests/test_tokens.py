from os import path

import pytest

import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from aap_client.tokens import TokenDecoder

from tests.payload_gen import payloadValidity

FOLDER = path.dirname(path.realpath(__file__)) +\
       u'/../resources/crypto_files/'

@pytest.fixture
def private_key():
    def _load_private(pem_filename, secret=None):
        with open(pem_filename, 'rb') as pem_file:
            private_key = load_pem_private_key(
                pem_file.read(),
                password=secret,
                backend=default_backend())
        return private_key

    return _load_private(FOLDER + u'disposable.private.pem')

DECODER_CONFIGS = [(u'disposable.public.pem', ['domains']),
                   (u'disposable.public.pem', None),
                   (u'disposable.public.der', None)]

@pytest.fixture(params=DECODER_CONFIGS)
def decoder(request):
    cert_filename, required_claims = request.param
    return TokenDecoder(FOLDER + cert_filename, required_claims=required_claims)

@pytest.mark.parametrize('name,generator,valid', payloadValidity, ids=[name for (name, _, _) in payloadValidity])
def test_token_validation(name, generator, valid, private_key, decoder):
    for payload in generator.generate(10):
        token = jwt.encode(payload, private_key, algorithm=u'RS256')

        def decode(token, payload):
            # don't request audience if there isn't any in the token
            aud = u'webapp.ebi.ac.uk' if u'aud' in payload else None
            decoder.decode(token, audience=aud)

        if valid:
            decode(token, payload)
        else:
            with pytest.raises(Exception) as e_info:
                decode(token, payload)
