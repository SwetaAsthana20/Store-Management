from flask_restful import reqparse, Resource
from Models.User import UserModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt)
from blacklist import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument("username",
                    type=str,
                    required = True,
                    help = "Field can't be empty."
)
_parser.add_argument("password",
                    type=str,
                    required=True,
                    help="Field can't be empty."
                    )

class UserSignUp(Resource):

    def post(self):
        data = _parser.parse_args()
        if UserModel.fetch_by_username(data["username"]):
            return {"message": "User with same name already exists, Try Logging in."}
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "Successfully signed up , THANK YOU :)"}


class User_info(Resource):

    def get(self, user_id):
        user = UserModel.fetch_by_id(user_id)
        if not user:
            return {"message": "User does not exist with this id"}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.fetch_by_id(user_id)
        if not user:
            return {"message": "User does not exist with this id"}, 404
        try:
            user.delete_from_db()
            return {"message": "user deleted successfully"}, 200
        except Exception as e:
            return {"message": f"Error occur while deleting{e}"}


class UserLogin(Resource):

    def post(self):
        data = _parser.parse_args()
        user = UserModel.fetch_by_username(data["username"])
        if user and user.password == data["password"]:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        else:
            return {"msg": "Authentication failed, No such user found"}, 404

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  ##jti is a unique id for each access token
        BLACKLIST.add(jti)
        return {"message":"Successfully logged out"}

class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        id = get_jwt_identity()
        refresh_token = create_access_token(identity=id,fresh=False)
        return {"access_token":refresh_token}, 200



