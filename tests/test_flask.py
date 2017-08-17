from __future__ import print_function
from os import path

import unittest2

import json

from flask import Flask, jsonify

from aap_client.crypto_files import load_public_from_x509
from aap_client.tokens import TokenEncoder
from aap_client.flask.client import JWTClient
from aap_client.flask.decorators import jwt_required, jwt_optional

from tests.payload_gen import validPayloads, invalidPayloads


class FlaskDecoratorsTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        folder = path.dirname(path.realpath(__file__)) + u'/../resources/crypto_files/'
        pem = folder + u'disposable.private.pem'
        x509 = folder + u'disposable.public.pem'

        cls._encoder = TokenEncoder(pem)

        cls.app = Flask(__name__)
        cls.app.public_key = load_public_from_x509(x509)

        cls.jwt_client = JWTClient(cls.app)
        cls.client = cls.app.test_client()

        @cls.app.route(u'/required')
        @jwt_required
        def required():
            return jsonify({u'msg': u'required'})

        @cls.app.route(u'/optional')
        @jwt_optional
        def optional():
            return jsonify({u'msg': u'optional'})

    def _request(self, verb, url, token=None, data=None):
        kwargs = dict()

        if verb == u'post':
            request = self.client.post
        else:
            request = self.client.get

        if token is not None:
            kwargs[u'headers'] = {u'Authorization': u'Bearer {}'.format(token)}
        if data is not None:
            kwargs[u'data'] = data

        response = request(url, **kwargs)

        if response.status_code == 303:
            kwargs.pop(u'data')
            response = self.client.get(response.headers[u'Location'], **kwargs)

        status_code = response.status_code
        data = json.loads(response.get_data(as_text=True))

        return status_code, data

    def test_valid_claims(self):
        payload = next(validPayloads[0][1].generate(1))
        token = self._encoder.encode(payload)

        status, _ = self._request(u'get', u'/required', token)
        self.assertEqual(status, 200)

        status, _ = self._request(u'get', u'/optional', token)
        self.assertEqual(status, 200)

    def test_no_token(self):
        status, _ = self._request(u'get', u'/required')
        self.assertEqual(status, 401)

        status, _ = self._request(u'get', u'/optional')
        self.assertEqual(status, 200)

    def test_invalid_claims(self):
        payload = next(invalidPayloads[0][1].generate(1))
        token = self._encoder.encode(payload)

        status, _ = self._request(u'get', u'/required', token)
        self.assertEqual(status, 401)

        status, _ = self._request(u'get', u'/optional', token)
        self.assertEqual(status, 200)


if __name__ == u'__main__':
    unittest2.main()
