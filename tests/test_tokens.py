from os import path

import unittest2

from aap_client.tokens import TokenEncoder, TokenDecoder

from tests.payload_gen import payloadValidity


class TokenTestCase(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = path.dirname(path.realpath(__file__)) + '/../resources/crypto_files/'
        cls._encoder = TokenEncoder(folder + 'disposable.private.pem')
        cls._decoder = TokenDecoder(folder + 'disposable.public.pem')

    def test_token(self):
        for (name, generator, valid) in payloadValidity:
            with self.subTest(token=name):
                for payload in generator.generate(10):
                    token = self._encoder.encode(payload)

                    # shouldn't request audience if there isn't any in the token
                    aud = 'webapp.ebi.ac.uk' if 'aud' in payload else None
                    decode = lambda tok: self._decoder.decode(tok, audience=aud)

                    if valid:
                        decode(token)
                    else:
                        with self.assertRaises(Exception) as c:
                            decode(token)


if __name__ == '__main__':
    unittest2.main()
