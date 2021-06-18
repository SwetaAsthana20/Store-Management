from db_conn_sqlalchemy import db

class StoreModel(db.Model):
    __tablename__ = "Store"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))
    Items = db.relationship("ItemModel", lazy= "dynamic")

    def __init__(self, name):
        self.Name = name

    def json(self):
        return {"Name": self.Name,
                "Items":[item.json() for item in self.Items.all()],
                "id": self.id}

    def save_to_db(self):
        db.session.add(self)
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