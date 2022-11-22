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
    '''Refresh access token.

    This is a helper method to request a new access token from auth0.

    return the access token.
    '''

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
    '''Get access token.

    This is a helper method to get the access token from environment variables
    if it's not valid a new token is requested from auth0 and the env variable
    is updated.

    return the access token.
    '''
    access_token = os.getenv("AUTH0_ACCESS_TOKEN")

    try:
        verify_decode_jwt(token=access_token,
                          audience=AUDIENCE_MANAGEMENT_API,
                          algorithms=ALGORITHMS,
                          auth0_domain=AUTH0_DOMAIN)
    except Exception:
        access_token = _refresh_access_token()
        os.environ["AUTH0_ACCESS_TOKEN"] = access_token

    return access_token


@users_blueprint.route('/users')
@requires_auth('read:users')
def get_users(payload):
    '''Retrieve details of users.

    auth:
        require the 'read:users' permission
    retun:
        - if success:
            - status code 200
            - json {"success": True, "users": data}
                users is a list of detailled description of users
    '''
    access_token = _get_access_token()

    headers = {'authorization': f"Bearer {access_token}"}
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        abort(500)

    data = response.json()

    return jsonify({"success": True, "users": data})


@users_blueprint.route('/users/<id>/roles')
@requires_auth('read:role')
def get_user_roles(payload, id):
    '''List the the roles associated with a user

    auth:
        require the 'read:role' permission
    params:
        id: a user's id.
    retun:
        - if success:
            - status code 200
            - json {"success": True, "roles": data}
                roles (a list) of a given user identified by id.
    '''
    access_token = _get_access_token()

    headers = {'authorization': f"Bearer {access_token}"}
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{id}/roles"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        abort(500)

    data = response.json()

    return jsonify({"success": True, "roles": data})


@users_blueprint.route('/users/<id>/organizations')
@requires_auth('read:organizations')
def get_user_organizations(payload, id):
    '''Retrieve all organizations that the specified user is a member of.

    auth:
        require the 'read:organizations' permission
    params:
        id: a user's id.
    retun:
        - if success:
            - status code 200
            - json {"success": True, "organizations": data}
                organizations that a given user is a member of.
    '''
    access_token = _get_access_token()

    headers = {'authorization': f"Bearer {access_token}"}
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{id}/organizations"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        abort(500)

    data = response.json()

    return jsonify({"success": True, "organizations": data})


@users_blueprint.route('/users/<id>/logs')
@requires_auth('read:logs_users')
def get_user_logs_events(payload, id):
    '''Retrieve log events for a specific user.

    auth:
        require the 'read:logs_users' permission
    params:
        id: a user's id.
    retun:
        - if success:
            - status code 200
            - json {"success": True, "logs": data}
                a given user's logs events.
    '''
    access_token = _get_access_token()

    headers = {'authorization': f"Bearer {access_token}"}
    url = f"https://{AUTH0_DOMAIN}/api/v2/users/{id}/logs"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        abort(500)

    data = response.json()

    return jsonify({"success": True, "logs": data})
