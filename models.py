import os
from flask.ext.login import UserMixin
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from api import db


class Bucketlist(db.Model):
    """
    The bucketlist model class.
    Attributes:
        id: Id of the bucketlist.
        name: Name of the bucketlist.
        date_created: Date bucketlist was created.
        date_modified: Date bucketlist was modified.
        items: Relationship field between the bucketlist and its items.
        created_by: The id of user who created the bucketlist.

    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    bl_items = db.relationship('Item')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Item(db.Model):
    """
    The bucketlist item model class.
    Attributes:
        id: The id of the bucketlist item.
        name: The name of the bucketlist item.
        date_created: Date bucketlist item was created.
        date_modified: Date bucketlist item was modified.
        bucketlist_id: ID of bucketlist which owns the item.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))


class User(db.Model, UserMixin):
    """
    The user model class.
    Attributes:
        id: The user id.
        username: The user's username which should be unique.
        email:The user's email which should be unique.
        password:Th user's password.
        bucketlists: Relationship field between the user and his bucketlists.
    Methods:
        hash_password: Hashes a new user's password.
        verify_password: Verify a user password.
        generate_auth_token: Generates the token using password and id
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    bucketlists = db.relationship('Bucketlist')

    def hash_password(self, password):
        """
        Hashes the users password
        Args:
            password: The password to be hashed.
        Returns:
            The hashed password.
        """

        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """Verify a password against an existing hash.
        Args:
            self.password: The inputed password by the user
        Returns:
            True if password hashes matches
            False if password hashes do not match.
        """
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self):
        """Generates authentication token.
        Args:
            data: takes the user id and hashed password and put in a list.
        Returns:
            A signed string serialized with the internal serializer.
        """
        serial = Serializer(os.environ.get('SECRET'), expires_in=180000)
        data = [str(self.id), self.password]
        return serial.dumps(data)
