from flask_restful import Resource, reqparse
from resource.models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import random
import json
import bcrypt

parser = reqparse.RequestParser()


class UserRegistration(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('password', help='This field cannot be blank')

    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        salt = bcrypt.gensalt().decode("utf-8")
        new_user = UserModel(
            username=data['username'],
            group='user',
            salt=salt,
            password=UserModel.generate_hash(data['password'] + salt)
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


# ------------------------------------------------------------------------
class UserLogin(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('password', help='This field cannot be blank')

    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        if UserModel.verify_hash(data['password'] + current_user.salt, current_user.password):
            access_token = create_access_token(identity={"username": data['username'], "group": current_user.group})
            refresh_token = create_refresh_token(identity={"username": data['username'], "group": current_user.group})
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}, 401


# -----------------------------------------------------------------------------
class AdminAddToGroup(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('group', help='This field cannot be blank')

    @jwt_required()
    def post(self):
        data = parser.parse_args()
        token = get_jwt_identity()
        if token["group"] == "admin":
            user = UserModel.find_by_username(data["username"])
            if user:
                UserModel.admin_add_to_group(data["username"], data["group"])
                return {'message': 'users add to entered group successfully'}
            else:
                return {'message': 'this users not exist'}
        else:
            return {'message': 'you have not access to this api'}


# ---------------------------------------------------------------------------
class AdminCreateAdmin(Resource):
    parser.add_argument('username', help='This field cannot be blank')
    parser.add_argument('password', help='This field cannot be blank')

    @jwt_required()
    def post(self):
        data = parser.parse_args()
        token = get_jwt_identity()
        if token["group"] == "admin":
            user = UserModel.find_by_username(data["username"])
            if user:
                return {'message': 'this users already exist'}
            else:
                salt = bcrypt.gensalt().decode("utf-8")
                new_user = UserModel(
                    username=data['username'],
                    group='admin',
                    salt=salt,
                    password=UserModel.generate_hash(data['password'] + salt)
                )
                new_user.save_to_db()
                access_token = create_access_token(identity={"username": data['username'], "group": "users"})
                refresh_token = create_refresh_token(identity={"username": data['username'], "group": "users"})
                return {
                    'message': 'User {} was created'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
        else:
            return {'message': 'you have not access to this api'}
