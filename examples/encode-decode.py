import os

from calendar import timegm
from datetime import datetime

from aap_client.token_encoder import TokenEncoder
from aap_client.token_decoder import TokenDecoder


dir = os.path.dirname(os.path.realpath(__file__)) + '/../resources/crypto_files/'
encoder = TokenEncoder(dir + 'disposable.private.pem')
decoder = TokenDecoder(dir + 'disposable.public.pem')


payload = {
    'exp': timegm(datetime.utcnow().utctimetuple()) + 15,
    'claim': 'example'
}

token = encoder.encode(payload)
print token

decoded = decoder.decode(token)
print decoded

