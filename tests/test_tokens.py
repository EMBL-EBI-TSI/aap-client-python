from os import path

import unittest2

from aap_client.tokens import TokenEncoder, TokenDecoder

from tests.payload_gen import payloadValidity


class TokenTestCase(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = path.dirname(path.realpath(__file__)) +\
                 u'/../resources/crypto_files/'
        cls._encoder = TokenEncoder(folder + u'disposable.private.pem')
        cls._decoder = TokenDecoder(folder + u'disposable.public.pem')

    def test_token(self):
        for (name, generator, valid) in payloadValidity:
            with self.subTest(token=name):
                for payload in generator.generate(10):
                    token = self._encoder.encode(payload)

                    # don't request audience if there isn't any in the token
                    aud = u'webapp.ebi.ac.uk' if u'aud' in payload else None

                    def decode(tok):
                        self._decoder.decode(tok, audience=aud)

                    if valid:
                        decode(token)
                    else:
                        with self.assertRaises(Exception):
                            decode(token)


if __name__ == u'__main__':
    unittest2.main()
