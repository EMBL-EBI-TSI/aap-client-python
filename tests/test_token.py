from future.utils import viewitems
from os import sys, path

import unittest2
import testdata

from aap_client.token_encoder import TokenEncoder
from aap_client.token_decoder import TokenDecoder

from tests.payload_gen import payloadValidity

class TokenTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        dir = path.dirname(path.realpath(__file__)) + '/../resources/crypto_files/'
        cls._encoder = TokenEncoder(dir + 'disposable.private.pem')
        cls._decoder = TokenDecoder(dir + 'disposable.public.pem')

    def test_token(self):
        for (name, generator, valid) in payloadValidity:
            with self.subTest(token=name):
                for payload in generator.generate(10):
                    token = self._encoder.encode(payload)

                    # shouldn't request audience if there isn't any in the token
                    aud = 'webapp.ebi.ac.uk' if 'aud' in payload else None
                    decode = lambda token: self._decoder.decode(token, audience=aud)

                    if valid:
                        decode(token)
                    else:
                        with self.assertRaises(Exception) as c:
                            decode(token)

if __name__ == '__main__':
    unittest2.main()
