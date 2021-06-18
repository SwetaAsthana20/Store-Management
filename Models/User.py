from db_conn_sqlalchemy import db

class UserModel(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"id": self.id, "username": self.username}

    @classmethod
    def fetch_by_username(cls, username):
        return cls.query.filter_by(username= username).first()

    @classmethod
    def fetch_by_id(cls, Id):
        return cls.query.filter_by(id = Id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
