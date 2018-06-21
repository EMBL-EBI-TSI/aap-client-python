from os import path

import pytest

import jwt

from aap_client.crypto_files import load_private_from_pem
from aap_client.tokens import TokenDecoder

from tests.payload_gen import payloadValidity


FOLDER = path.dirname(path.realpath(__file__)) +\
       u'/../resources/crypto_files/'
KEY = load_private_from_pem(FOLDER + u'disposable.private.pem')
DECODER = TokenDecoder(FOLDER + u'disposable.public.pem')


@pytest.mark.parametrize('name,generator,valid', payloadValidity, ids=[name for (name, _, _) in payloadValidity])
def test_token_validation(name, generator, valid):
    for payload in generator.generate(10):
        token = jwt.encode(payload, KEY, algorithm=u'RS256')

        # don't request audience if there isn't any in the token
        aud = u'webapp.ebi.ac.uk' if u'aud' in payload else None

        def decode(tok):
            DECODER.decode(tok, audience=aud)

        if valid:
            decode(token)
        else:
            with pytest.raises(Exception) as e_info:
                decode(token)
