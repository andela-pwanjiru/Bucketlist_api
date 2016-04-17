import os
from flask.ext.login import UserMixin
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from api import db


class Bucketlist(db.Model):
    """Stores Bucketlists."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    bl_items = db.relationship('Item')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Item(db.Model):
    """Stores Bucketlist Items"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))


class User(db.Model, UserMixin):
    """Stores users"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    bucketlists = db.relationship('Bucketlist')

    def hash_password(self, password):
        """Hashes the password """
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """Verify a password against an existing hash"""
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self):
        """Generates authentication token."""
        serial = Serializer(os.environ.get('SECRET'), expires_in=1800)
        data = [str(self.id), self.password]
        return serial.dumps(data)
