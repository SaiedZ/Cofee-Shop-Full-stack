from flask import Flask
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db # noqa
from .utils import error_handlers
from .users.users import users_blueprint
from .drinks.drinks import drinks_blueprint

app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(drinks_blueprint)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()
