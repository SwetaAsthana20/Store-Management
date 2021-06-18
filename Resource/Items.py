from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from Models.Items import ItemModel



class Items(Resource):
    @jwt_required()
    def get(self):
        if get_jwt().get("ID") <10:
            return {"Items": [item.json() for item in ItemModel.find_all()]}
        else:
            return {"message": "Access denied"}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("Price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument("Store_id",
                        type=int,
                        required=True,
                        help="Assign a store id")

    def get(self, name):
        row = ItemModel.fetch_by_name(name)
        if row:
            return row.json()
        return "Item Not Found", 404

    def post(self, name):
        row = ItemModel.fetch_by_name(name)
        if row:
            return "Item already exist.", 400

        data = Item.parser.parse_args()
        data = ItemModel(name, data["Price"], data["Store_id"])
        try:
            data.save_to_db()
        except:
            return {"message": "Error occurred while saving the data"}, 500
        return f'Saved item details', 201

    @jwt_required(fresh=True)
    def delete(self, name):
        item = ItemModel.fetch_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item Deleted"}, 200
        else:
            return {"message": "Item Not Found"}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.fetch_by_name(name)
        try:
            if not item:
                item = ItemModel(name, data["Price"], data["Store_id"])
                item.save_to_db()
            else:
                item.Price = data["Price"]
                item.Store_id = data["Store_id"]
                item.update_to_db()
        except:
            return {"message": "Error occurred while saving the data"}, 500

        return "Saved item details", 201
