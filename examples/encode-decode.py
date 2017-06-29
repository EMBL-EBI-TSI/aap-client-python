import os

from calendar import timegm
from datetime import datetime

from aap_client.token_encoder import TokenEncoder
from aap_client.token_decoder import TokenDecoder


dir = os.path.dirname(os.path.realpath(__file__)) + '/../resources/crypto_files/'
encoder = TokenEncoder(dir + 'disposable.private.pem')
decoder = TokenDecoder(dir + 'disposable.public.pem')


payload = {
    'iat': timegm(datetime.utcnow().utctimetuple()),
    'exp': timegm(datetime.utcnow().utctimetuple()) + 15,
    'sub': 'usr-a1d0c6e83f027327d8461063f4ac58a6',
    'name': 'John Doe',
    'nickname': '73475cb40a568e8da8a045ced110137e159f890ac4da883b6b17dc651b3a8049',
    'email': 'subject@ebi.ac.uk'
}

token = encoder.encode(payload)
print token

decoded = decoder.decode(token)
print decoded

