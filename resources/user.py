
from models.user import UserModel

from flask_restful import Resource,reqparse


class UserRegister(Resource):
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
        data = UserRegister.parser.parse_args()

        #check tài khoản đã tồn tại chưa
        if UserModel.find_by_username(data['username']):
            return 'the user already exists'

        user = UserModel(data['username'] , data['password'])
        user.save_to_db()


        # connection = sqlite3.connect('data.sqlite')
        # cursor = connection.cursor()

        # query = "INSERT INTO users VALUES (NULL,?,?)"
        # cursor.execute(query,(data['username'] , data['password']))

        # connection.commit()

        # connection.close()

        return {'message' : 'User created successfully'}


    