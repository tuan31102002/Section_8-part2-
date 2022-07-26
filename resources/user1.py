from flask import request
from flask_jwt_extended import create_access_token
from models.user import UserModel

from flask_restful import Resource
from flask_restful import Resource,reqparse

class UserRegister1(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required = True,
        help = "This field cannot be blank")

    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be blank")

    def post(self):
        data = UserRegister1.parser.parse_args()

        if UserModel.find_by_username(data['username']):
             return 'the user already exists'
        user = UserModel(data['username'] , data['password'])
        user.save_to_db()

        access_token = create_access_token(identity=data['username'])
        
        return {'User created successfully , access_token' : access_token}

