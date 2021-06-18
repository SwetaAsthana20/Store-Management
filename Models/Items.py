from db_conn_sqlalchemy import db

class ItemModel(db.Model):
    __tablename__ = "Items"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))
    Price = db.Column(db.Float(precision = 2))

    Store_id = db.Column(db.Integer, db.ForeignKey("Store.id"))
    Store = db.relationship("StoreModel")


    def __init__(self, name, price, store_id):
        self.Name = name
        self.Price = price
        self.Store_id = store_id

    def json(self):
        return {"id": self.id,
                "Name": self.Name,
                "Price": self.Price,
                "Store_id": self.Store_id,
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        ItemModel.query.filter_by(Name = self.Name).update(dict(Price= self.Price, Store_id= self.Store_id))
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_by_name(cls,name):
        return cls.query.filter_by(Name = name).first() ##SELECT *FROM Items WHERE NAME="name" LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()