import hashlib

from calendar import timegm
from datetime import datetime

from builtins import int

import testdata

def now():
    return timegm(datetime.utcnow().utctimetuple())

class PayloadFactory(testdata.DictFactory):
    iat = testdata.Constant(now())
    exp = testdata.RandomInteger(int(now() + 15), int(now() * 2))
    iss = testdata.Constant('aap.ebi.ac.uk')
    sub = testdata.Sum([testdata.Constant('usr-'), testdata.HashHexDigestFactory(hashlib.md5)])
    email = testdata.FakeDataFactory('email')
    name = testdata.FakeDataFactory('name')
    nickname = testdata.HashHexDigestFactory(hashlib.sha256)

payloadValidity = [
    ('There is absolutely no cause for alarm',
     PayloadFactory(),
     True),

    ('Expired',
     PayloadFactory(
        iat=testdata.RandomInteger(0,            now() - 3600),
        exp=testdata.RandomInteger(now() - 3600, now() - 1)
    ), False),

    ('No expiration',
     PayloadFactory(
        exp=testdata.Constant(None)
    ), False),

    # Standard says iat should be a number, shouldn't care when it's issued
    # yay for sanity checks, I guess
    ('Back to the future',
     PayloadFactory(
        iat=testdata.RandomInteger(now() + 3600,  now() * 2),
        exp=testdata.RandomInteger(now() * 2 + 1, now() * 3)
    ), True),

    ('No issue time',
     PayloadFactory(
        iat=testdata.Constant(None)
    ), False),

    ('Untrusted issuer',
     PayloadFactory(
         iss=testdata.FakeDataFactory('address')
     ), True),

    ('Untrusted issuer',
     PayloadFactory(
        iss=testdata.Constant(None)
     ), True),

    ('Unknown audience',
     PayloadFactory(
        aud=testdata.Constant('portal.ebi.ac.uk')
     ), False),

    ('Known audience',
     PayloadFactory(
        aud=testdata.Constant('webapp.ebi.ac.uk')
     ), True),

    ('No subject',
     PayloadFactory(
        sub=testdata.Constant(None)
     ), False),

    ('No email',
     PayloadFactory(
        email=testdata.Constant(None)
     ), False),

    ('No name',
     PayloadFactory(
        name=testdata.Constant(None)
     ), False),

    ('No nickname',
     PayloadFactory(
        nickname=testdata.Constant(None)
     ), False),
]

if __name__ == '__main__':
    for payload in PayloadFactory().generate(10):
        print payload
