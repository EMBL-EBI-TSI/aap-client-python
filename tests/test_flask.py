from __future__ import print_function
from os import path

import pytest

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

@pytest.fixture
def key_public_private():
    folder = path.dirname(path.realpath(__file__)) +\
             u'/../resources/crypto_files/'
    private = load_private_from_pem(folder + u'disposable.private.pem')
    public = load_public_from_x509(folder + u'disposable.public.pem')
    return public, private

@pytest.fixture
def flask_server_client(key_public_private):
    app = Flask(__name__)
    app.config[u'JWT_PUBLIC_KEY'] = key_public_private[0]

    jwt_client = JWTClient(app)
    client = app.test_client()

    @app.route(u'/required')
    @jwt_required
    def required():
        return jsonify({u'message': u'required'})

    @app.route(u'/optional')
    @jwt_optional
    def optional():
        return jsonify({u'message': u'optional'})

    return app, client

@pytest.fixture
def valid_token_payload(key_public_private):
    _, private = key_public_private

    payload = next(validPayloads[0][1].generate(1))
    token = jwt.encode(payload, private, algorithm=u'RS256')
    return token, payload

@pytest.fixture
def invalid_token_payload(key_public_private):
    _, private = key_public_private

    payload =  next(invalidPayloads[0][1].generate(1))
    token = jwt.encode(payload, private, algorithm=u'RS256')
    return token, payload

def request(client, verb, url, token=None, data=None, custom_auth=False):
    kwargs = dict()

    if verb == u'post':
        request = client.post
    else:
        request = client.get

    if token is not None:
        if not custom_auth:
            a_header = u'Bearer {}'.format(token.decode('utf-8'))
        else:
            a_header = token.decode('utf-8')
        kwargs[u'headers'] =\
            {u'Authorization': a_header}
    if data is not None:
        kwargs[u'data'] = data

    response = request(url, **kwargs)

    if response.status_code == 303:
        kwargs.pop(u'data')
        response = client.get(response.headers[u'Location'], **kwargs)

    status_code = response.status_code
    data = json.loads(response.get_data(as_text=True))
    headers = response.headers

    return status_code, data, headers

def test_no_token(flask_server_client):
    _, client = flask_server_client

    status, _, _ = request(client, u'get', u'/required')
    assert status == 401

    status, _, _ = request(client, u'get', u'/optional')
    assert status == 200

def test_valid_claims(flask_server_client, valid_token_payload):
    _, client = flask_server_client
    token, _ = valid_token_payload

    status, message, _ = request(client, u'get', u'/required', token)
    assert message == {u'message': u'required'}
    assert status == 200

    status, _, _ = request(client, u'get', u'/optional', token)
    assert status == 200

def test_invalid_claims(flask_server_client, invalid_token_payload):
    _, client = flask_server_client
    token, _ = invalid_token_payload

    status, _, _ = request(client, u'get', u'/required', token)
    assert status == 401

    status, _, _ = request(client, u'get', u'/optional', token)
    assert status == 200

def test_malformed_token(flask_server_client):
    _, client = flask_server_client
    token = b'foo'

    status, _, _ = request(client, u'get', u'/required', token)
    assert status == 401

    status, _, _ = request(client, u'get', u'/optional', token)
    assert status == 200

invalid_auth_headers = [b'foo', b'foo bar', b'Bearer ']
@pytest.mark.parametrize('token',
                         invalid_auth_headers,
                         ids=[b.decode('utf-8') for b in invalid_auth_headers])
def test_invalid_request(token, flask_server_client):
    _, client = flask_server_client

    status, _, _ = request(client, u'get', u'/required', token, custom_auth=True)
    assert status == 400

    status, _, _ = request(client, u'get', u'/optional', token, custom_auth=True)
    assert status == 400

def test_get_claims(key_public_private,
                    flask_server_client,
                    valid_token_payload):
    public, _ = key_public_private
    app, client = flask_server_client
    token, payload = valid_token_payload

    app.config[u'JWT_PUBLIC_KEY'] = public

    @app.route(u'/test')
    @jwt_required
    def claim_validator():
        claims = get_claims()
        assert claims is not None
        assert u'sub' in claims
        assert payload == claims
        return jsonify({u'message': u'required'})

    client.get(u'/test',
               headers={u'Authorization': u'Bearer {}'.format(
                   token.decode('utf-8'))}
              )
