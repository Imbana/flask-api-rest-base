from datetime import datetime
from services.database import db
from .bookmarks import Bookmark

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship(Bookmark, backref="user")

    # def __repr__(self):
    #     return 'User>>> {self.username}'

    # def __init__(self, fullname, email, phone)
    #     self.fullname = fullname
    #     self.email = email
    #     self.phone = phone