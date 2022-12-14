import json

import flask
from flask import request, jsonify, abort
from sqlalchemy import exc

from ..database.models import Drink
from ..auth.auth import requires_auth

drinks_blueprint = flask.Blueprint('drinks_blueprint', __name__)


@drinks_blueprint.route('/drinks')
def get_drinks():
    '''Get all the drinks.

    auth:
        public method.
    retun:
        - if success:
            - status code 200
            - json {"success": True, "drinks": drinks}
                drinks is a list of short description of a drink
        -if fail:
            - status code 422
    '''
    try:
        drinks = [
            drink.short() for drink in Drink.query.all()
        ]
    except Exception:
        abort(422)

    return jsonify({"success": True, "drinks": drinks})


@drinks_blueprint.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    '''Get all the drinks detail.

    auth:
        require the 'get:drinks-detail' permission
    retun:
        - if success:
            - status code 200
            - json {"success": True, "drinks": drinks}
                drinks is a list of detailled description of a drink
    '''
    try:
        drinks = [
            drink.short() for drink in Drink.query.all()
        ]
    except Exception:
        abort(422)

    return jsonify({"success": True, "drinks": drinks})


@drinks_blueprint.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    '''Creates a new drink.

    auth:
        requires the 'post:drinks' permission
    retun:
        - if success:
            - status code 200
            - json {"success": True, "drinks": drinks}
                drink an array containing only the newly created drink
                with drink.long() data representation
    '''
    data = request.get_json()
    if data is None:
        abort(400, 'The drink\'s title and recipe not found.')

    try:
        title, recipe = data['title'], data['recipe']
    except ValueError:
        abort(400, 'Drink data must contain title and recipe')
    if not isinstance(recipe, (list, dict)):
        abort(400, 'Recipe must be a json object')
    if isinstance(recipe, dict):
        # to avoid error because different format between postman and frontend
        recipe = [recipe]
    try:
        new_drink = Drink(
            title=title,
            recipe=json.dumps(recipe),
        )
        new_drink.insert()
    except exc.IntegrityError:
        abort(400, 'A drink with that title aldready exist')
    except Exception:
        abort(500)

    return jsonify({"success": True, "drinks": [new_drink.long()]})


@drinks_blueprint.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    '''Updates an existing drink base on the id.

    auth:
        requires the 'patch:drinks' permission
    retun:
        - if success:
            - status code 200
            - json {"success": True, "drinks": drinks}
                drink an array containing only the newly updated drink
                with drink.long() data representation
        - 404 if id not found
    '''
    drink = Drink.query.get_or_404(id)

    data = request.get_json()
    if data is None:
        abort(400, 'No data was found.')

    drink.title = data.get('title') or drink.title
    drink.recipe = data.get('recipe') or drink.recipe

    try:
        drink.update()
    except Exception:
        abort(500)

    return jsonify({"success": True, "drinks": [drink.long()]})


@drinks_blueprint.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    '''Deletes an existing drink based on the id.

    auth:
        requires the 'delete:drinks' permission
    retun:
        - if success:
            - status code 200
            - json {"success": True, "delete": id}
                where id is the id of the deleted record
        - 404 if id not found
    '''

    drink = Drink.query.get_or_404(id)
    try:
        drink.delete()
    except Exception:
        abort(500)

    return jsonify({"success": True, "delete": id})
