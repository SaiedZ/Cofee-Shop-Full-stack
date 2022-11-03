import flask
from flask import jsonify

blueprint = flask.Blueprint('error_handlers', __name__)



@blueprint.app_errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            {"success": False,
                "error": 400,
                "message": error.description}
        ),
        400
    )


@blueprint.app_errorhandler(401)
def unauthorized(error):
    message = error.description
    return (
        jsonify(
            {"success": False,
                "error": 401,
                "message": message}
        ),
        401
    )


@blueprint.app_errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {"success": False,
                "error": 404,
                "message": error.description}
        ),
        404,
    )


@blueprint.app_errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    return (
        jsonify(
            {"success": False,
                "error": 500,
                "message": "Internal Server Error"}
        ),
        500
    )
