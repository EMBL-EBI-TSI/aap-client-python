from __future__ import absolute_import
from os import sys, path

from aap_client.tokens import TokenEncoder, TokenDecoder

sys.path.append(path.abspath(path.join(path.dirname(__file__), '../tests/')))
from payload_gen import PayloadFactory

dir = path.dirname(path.realpath(__file__)) + '/../resources/crypto_files/'
encoder = TokenEncoder(dir + 'disposable.private.pem')
decoder = TokenDecoder(dir + 'disposable.public.pem')


def main():
    for payload in PayloadFactory().generate(10):
        print
        print payload
        token = encoder.encode(payload)
        print token

        decoded = decoder.decode(token)
        assert payload == decoded

if __name__ == '__main__':
    main()
