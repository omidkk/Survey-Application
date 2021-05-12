from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

application = Flask(__name__)

# set FLASK_DEBUG=1 in command line
# set FLASK_ENV=development
# set FLASK_APP=application.py

application.config['ENV'] = 'development'
application.config['DEBUG'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'some-secret-string'
application.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

db = SQLAlchemy(application)
migrate = Migrate(application, db)

jwt = JWTManager(application)



@application.before_first_request
def create_tables():
    db.create_all()


api = Api(application)

import views
from resource import models
from services.users import user_services


#-------------------------------------users--------------------------------

api.add_resource(user_services.UserRegistration, '/registration')
api.add_resource(user_services.UserLogin, '/login')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()