import hashlib

from calendar import timegm
from datetime import datetime

from builtins import int

import testdata

def now():
    return timegm(datetime.utcnow().utctimetuple())

class ClaimsFactory(testdata.DictFactory):
    iat = testdata.Constant(now())
    exp = testdata.RandomInteger(int(now() + 15), int(now()*10))
    iss = 'aap.ebi.ac.uk'
    sub = testdata.Sum([testdata.Constant('usr-'), testdata.HashHexDigestFactory(hashlib.md5)])
    email = testdata.FakeDataFactory('email')
    name = testdata.FakeDataFactory('name')
    nickname = testdata.HashHexDigestFactory(hashlib.sha256)

if __name__ == '__main__':
    for claims in ClaimsFactory().generate(10):
        print claims
