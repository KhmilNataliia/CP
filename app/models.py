from flask_login import UserMixin
from app import db, login_manager, mdb
from flask_mongoengine import MongoEngine


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    login = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(60), index=True)
    surname = db.Column(db.String(60), index=True)
    phone = db.Column(db.String(20), index=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.login)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(mdb.Document):
    name = mdb.StringField(required=True)
    data = mdb.StringField(required=True)
    #url = mdb.StringField(required=True)
    #image = mdb.StringField()
    #price = mdb.StringField()
    #availability = mdb.StringField()
    #data = mdb.ListField(mdb.ListField(mdb.StringField()))
    meta = {}
