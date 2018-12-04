from __future__ import print_function
import hashlib

from calendar import timegm
from datetime import datetime

from builtins import int

import fake_gen


def now():
    return timegm(datetime.utcnow().utctimetuple())


class PayloadFactory(fake_gen.DictFactory):
    iat = fake_gen.Constant(now())
    exp = fake_gen.RandomInteger(int(now() + 15), int(now() * 2))
    iss = fake_gen.Constant(u'aap.ebi.ac.uk')
    sub = fake_gen.Sum([fake_gen.Constant(u'usr-'),
                        fake_gen.HashHexDigestFactory(hashlib.md5)])
    email = fake_gen.FakeDataFactory(u'email')
    name = fake_gen.FakeDataFactory(u'name')
    nickname = fake_gen.HashHexDigestFactory(hashlib.sha256)
    domains = fake_gen.Constant([])


payloadValidity = [
    (u'There is absolutely no cause for alarm',
     PayloadFactory(),
     True),

    (u'Expired',
     PayloadFactory(
         iat=fake_gen.RandomInteger(0,            now() - 3600),
         exp=fake_gen.RandomInteger(now() - 3600, now() - 1)
     ), False),

    (u'No expiration',
     PayloadFactory(
         exp=fake_gen.Constant(None)
     ), False),

    # Standard says iat should be a number, shouldn't care when it's issued
    # yay for sanity checks, I guess
    (u'Back to the future',
     PayloadFactory(
         iat=fake_gen.RandomInteger(now() + 3600,  now() * 2),
         exp=fake_gen.RandomInteger(now() * 2 + 1, now() * 3)
     ), True),

    (u'No issue time',
     PayloadFactory(
         iat=fake_gen.Constant(None)
     ), False),

    (u'Untrusted issuer',
     PayloadFactory(
         iss=fake_gen.FakeDataFactory(u'address')
     ), True),

    (u'Untrusted issuer',
     PayloadFactory(
         iss=fake_gen.Constant(None)
     ), True),

    (u'No subject',
     PayloadFactory(
         sub=fake_gen.Constant(None)
     ), False),

    (u'No email',
     PayloadFactory(
         email=fake_gen.Constant(None)
     ), False),

    (u'No name',
     PayloadFactory(
         name=fake_gen.Constant(None)
     ), False),

    (u'No nickname',
     PayloadFactory(
         nickname=fake_gen.Constant(None)
     ), False),
]

validPayloads = [(name, generator) for (name, generator, valid)
                 in payloadValidity if valid]
invalidPayloads = [(name, generator) for (name, generator, valid)
                   in payloadValidity if not valid]

if __name__ == u'__main__':
    for payload in PayloadFactory().generate(10):
        print(payload)
