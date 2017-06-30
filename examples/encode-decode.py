from __future__ import absolute_import
from os import sys, path

from aap_client.token_encoder import TokenEncoder
from aap_client.token_decoder import TokenDecoder

sys.path.append(path.abspath(path.join(path.dirname(__file__), '../tests/')))
from claims_gen import ClaimsFactory

dir = path.dirname(path.realpath(__file__)) + '/../resources/crypto_files/'
encoder = TokenEncoder(dir + 'disposable.private.pem')
decoder = TokenDecoder(dir + 'disposable.public.pem')


def main():
    for payload in ClaimsFactory().generate(10):
        print
        print payload
        token = encoder.encode(payload)
        print token

        decoded = decoder.decode(token)
        assert payload == decoded

if __name__ == '__main__':
    main()
