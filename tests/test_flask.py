from __future__ import print_function
from os import path

import unittest2

import json
import jwt

from flask import Flask, jsonify

from aap_client.crypto_files import (
    load_public_from_x509,
    load_private_from_pem
)
from aap_client.flask.client import JWTClient
from aap_client.flask.decorators import jwt_required, jwt_optional

from tests.payload_gen import validPayloads, invalidPayloads


class FlaskDecoratorsTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        folder = path.dirname(path.realpath(__file__)) +\
                 u'/../resources/crypto_files/'
        cls._key = load_private_from_pem(folder + u'disposable.private.pem')
        x509 = folder + u'disposable.public.pem'

        cls.app = Flask(__name__)
        cls.app.config[u'JWT_PUBLIC_KEY'] = load_public_from_x509(x509)

        cls.jwt_client = JWTClient(cls.app)
        cls.client = cls.app.test_client()

        @cls.app.route(u'/required')
        @jwt_required
        def required():
            return jsonify({u'message': u'required'})

        @cls.app.route(u'/optional')
        @jwt_optional
        def optional():
            return jsonify({u'message': u'optional'})

    def _request(self, verb, url, token=None, data=None):
        kwargs = dict()

        if verb == u'post':
            request = self.client.post
        else:
            request = self.client.get

        if token is not None:
            kwargs[u'headers'] =\
                {u'Authorization': u'Bearer {}'.format(token.decode('utf-8'))}
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
        token = jwt.encode(payload, self._key, algorithm=u'RS256')

        status, message = self._request(u'get', u'/required', token)
        self.assertEqual(message, {u'message': u'required'})
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
        token = jwt.encode(payload, self._key, algorithm=u'RS256')

        status, message = self._request(u'get', u'/required', token)
        self.assertIn(u'expired', message[u'message'])
        self.assertEqual(status, 401)

        status, _ = self._request(u'get', u'/optional', token)
        self.assertEqual(status, 200)

    def test_get_claims(self):
        payload = next(validPayloads[0][1].generate(1))
        token = jwt.encode(payload, self._key, algorithm=u'RS256')

        app = Flask(__name__)
        app.config[u'JWT_PUBLIC_KEY'] = self.app.config[u'JWT_PUBLIC_KEY']

        JWTClient(app)
        client = app.test_client()

        @app.route(u'/test')
        @jwt_required
        def required():
            claims = get_claims()
            self.assertIsNotNone(claims)
            self.assertIn(u'sub', claims)
            self.assertEqual(payload, claims)
            return jsonify({u'message': u'required'})

        client.get(u'/test',
                   headers={u'Authorization': u'Bearer {}'.format(
                       token.decode('utf-8'))}
                  )


if __name__ == u'__main__':
    unittest2.main()
