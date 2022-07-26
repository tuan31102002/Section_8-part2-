from flask import Flask, jsonify, request 
from flask_restful import Api,reqparse
from resources.user1 import UserRegister1
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models.user import UserModel

import hmac




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS-'] = False
# app.secret_key = 'jose'
api = Api(app)

app.config["JWT_SECRET_KEY"] = "jose"  # Change this!
jwt = JWTManager(app) 

# @app.before_first_request
# def create_tables():
#     db.create_all()


# jwt = JWT(app,authenticate,identity) #/auth

@app.route('/login' ,methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required = True,
        help = "This field cannot be blank")

    parser.add_argument('password',
        type = str,
        required = True,
        help = "This field cannot be blank")

    data = UserRegister1.parser.parse_args()

    user = UserModel.find_by_username(data['username'])
    if user is None:
             return {'message' : 'The user not found'}

    # if bcrypt.checkpw(data['password'].encode('utf-8'), user.hash):
    #     access_token = create_access_token(identity=data['username'])
    #     return {'access_token' : access_token}

    if user and hmac.compare_digest(user.password , data['password']):
        access_token = create_access_token(identity=data['username'])
        return {'access_token' : access_token}


@app.route('/test' ,methods=['GET'])
@jwt_required()
def test():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister1, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000 , debug=True) 