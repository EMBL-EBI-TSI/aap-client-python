from __future__ import print_function
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
    iss = testdata.Constant(u'aap.ebi.ac.uk')
    sub = testdata.Sum([testdata.Constant(u'usr-'),
                        testdata.HashHexDigestFactory(hashlib.md5)])
    email = testdata.FakeDataFactory(u'email')
    name = testdata.FakeDataFactory(u'name')
    nickname = testdata.HashHexDigestFactory(hashlib.sha256)
    domains = testdata.Constant([])


payloadValidity = [
    (u'There is absolutely no cause for alarm',
     PayloadFactory(),
     True),

    (u'Expired',
     PayloadFactory(
         iat=testdata.RandomInteger(0,            now() - 3600),
         exp=testdata.RandomInteger(now() - 3600, now() - 1)
     ), False),

    (u'No expiration',
     PayloadFactory(
         exp=testdata.Constant(None)
     ), False),

    # Standard says iat should be a number, shouldn't care when it's issued
    # yay for sanity checks, I guess
    (u'Back to the future',
     PayloadFactory(
         iat=testdata.RandomInteger(now() + 3600,  now() * 2),
         exp=testdata.RandomInteger(now() * 2 + 1, now() * 3)
     ), True),

    (u'No issue time',
     PayloadFactory(
         iat=testdata.Constant(None)
     ), False),

    (u'Untrusted issuer',
     PayloadFactory(
         iss=testdata.FakeDataFactory(u'address')
     ), True),

    (u'Untrusted issuer',
     PayloadFactory(
         iss=testdata.Constant(None)
     ), True),

    (u'No subject',
     PayloadFactory(
         sub=testdata.Constant(None)
     ), False),

    (u'No email',
     PayloadFactory(
         email=testdata.Constant(None)
     ), False),

    (u'No name',
     PayloadFactory(
         name=testdata.Constant(None)
     ), False),

    (u'No nickname',
     PayloadFactory(
         nickname=testdata.Constant(None)
     ), False),
]

validPayloads = [(name, generator) for (name, generator, valid)
                 in payloadValidity if valid]
invalidPayloads = [(name, generator) for (name, generator, valid)
                   in payloadValidity if not valid]

if __name__ == u'__main__':
    for payload in PayloadFactory().generate(10):
        print(payload)
