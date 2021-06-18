from flask_restful import Resource, reqparse
from Models.Stores import StoreModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class Stores(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("Name",
                        type = str,
                        required = True,
                        help = "Store name is required."
                        )
    def get(self, name):
        store  = StoreModel.fetch_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404


    def post(self, name):
        store = StoreModel.fetch_by_name(name)
        if store:
            return {"message": "Store already exists."}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {"message": "Error while saving data."}
        return {"message": "Successfully saved the data"}

    def delete(self,name):
        store = StoreModel.fetch_by_name(name)
        if store:
            store.delete_from_db()
        return {"message":"Successful deletion of data."}


class StoresList(Resource):
    @jwt_required(optional=True)
    def get(self):
        if get_jwt_identity():
            return {"Stores": [store.json() for store in StoreModel.find_all()]}
        else:
            return {"Stores": [store.Name for store in StoreModel.find_all()],
                   "Message": "More data available please login, if you want to see"}
