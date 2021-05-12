from flask_restful import Resource, reqparse
from resource.models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import json

parser = reqparse.RequestParser()


class UserRegistration(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('password', help='This field cannot be blank')

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            group='user'
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity={"username": data['username'], "group": "users"})
            refresh_token = create_refresh_token(identity={"username": data['username'], "group": "users"})
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500
#------------------------------------------------------------------------
class UserLogin(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('password', help='This field cannot be blank')
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity={"username": data['username'], "group": current_user.group})
            refresh_token = create_refresh_token(identity={"username": data['username'], "group": current_user.group})
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'} , 401
#-----------------------------------------------------------------------------