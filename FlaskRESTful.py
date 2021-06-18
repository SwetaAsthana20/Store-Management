import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from Resource.User import UserSignUp, User_info, UserLogin, TokenRefresh, UserLogout
from Resource.Items import Items, Item
from Resource.Stores import Stores, StoresList
from blacklist import BLACKLIST


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///datastore_sqlalchemy.db")
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"]= True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"]= ['access', 'refresh']
app.secret_key = 'SecurityPassword'
api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(decryption_info,jwt_info):
    return jwt_info.get("jti") in BLACKLIST

@jwt.revoked_token_loader
def revoked_token_callback(decrypted_token, jwt_info):
    return {
        "message":"token id revoked/ blacklisted.",
        "error": "token revoked"
    }

@jwt.additional_claims_loader
def additional_claims(identity):
    return {"ID": identity}


api.add_resource(Item, '/item/<string:name>', '/item_info/<string:name>', endpoint='get')
api.add_resource(Item, '/item/<string:name>')
# Giving endpoint is optional it will check the type of request and call the method.
api.add_resource(Item, '/item/<string:name>', '/item_info/<string:name>', endpoint='delete')
api.add_resource(Item, '/item/<string:name>', endpoint='put')
api.add_resource(Items, '/items', '/get_items', '/')

api.add_resource(UserSignUp, "/signup", endpoint="post")
api.add_resource(User_info, "/user_info/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh login")
api.add_resource(UserLogout,"/logout")

api.add_resource(Stores, "/store/<string:name>")
api.add_resource(StoresList, "/stores/")

if __name__ == "__main__":
    from db_conn_sqlalchemy import db
    db.init_app(app)
    app.run(port=5001)
