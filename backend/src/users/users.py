import os
import json
import requests

import flask
from flask import jsonify, abort

from ..auth.auth import verify_decode_jwt
from ..auth.auth import requires_auth

users_blueprint = flask.Blueprint('users_blueprint', __name__)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = os.getenv("ALGORITHMS")
CLIENT_ID_MANAGEMENT_API = os.getenv("CLIENT_ID_MANAGEMENT_API")
CLIENT_SECRET_MANAGEMENT_API = os.getenv("CLIENT_SECRET_MANAGEMENT_API")
AUDIENCE_MANAGEMENT_API = os.getenv("AUDIENCE_MANAGEMENT_API")


def _refresh_access_token():

    payload_dict = {
        "client_id": CLIENT_ID_MANAGEMENT_API,
        "client_secret": CLIENT_SECRET_MANAGEMENT_API,
        "audience": AUDIENCE_MANAGEMENT_API,
        "grant_type": "client_credentials"
    }
    payload = json.dumps(payload_dict)
    headers = {'content-type': "application/json"}

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    res = requests.post(url, data=payload, headers=headers)
    data = res.json()

    return data["access_token"]


def _get_access_token():

    access_token = os.getenv("AUTH0_ACCESS_TOKEN")

    try:
        verify_decode_jwt(token=access_token,
                          audience=AUDIENCE_MANAGEMENT_API,
                          algorithms=ALGORITHMS,
                          auth0_domain=AUTH0_DOMAIN)
    except Exception:
        access_token = _refresh_access_token()
        os.environ["AUTH0_ACCESS_TOKEN"] = access_token

    print(access_token)
    return access_token


@users_blueprint.route('/users')
@requires_auth('read:users')
def get_users(payload):

    access_token = _get_access_token()

    headers = {'authorization': f"Bearer {access_token}"}
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"

    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        abort(500)

    data = response.json()

    return jsonify(data)
