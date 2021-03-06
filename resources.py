import time
from flask import request
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequestKeyError
from flask.ext.login import login_required, current_user
from flask_restful import Resource, fields, marshal
import models
from api import db


bucketlist_item_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}

bucketlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'bl_items': fields.Nested(bucketlist_item_fields),
    'created_by': fields.String
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'online': fields.Boolean,
    'bucketlists': fields.Nested(bucketlist_fields)
}


class Bucketlists(Resource):
    """Resource for showing and handling all actions on bucketlists.
    Endpoint:
        '/bucketlists/'
    Methods:
        'GET', 'POST'
    """

    decorators = [login_required]

    def get(self):
        """
        List bucketlists from authenticated user.
        Args:
            self
        Return:
            All bucketlists belonging to the logged in user.
        """

        try:
            page = int(request.args['page'])
            # `limit` specifies the number of results
            # Get the limit specified by the user
            limit = int(request.args['limit'])
            # If limit specified isn't number type, set to 20
        except BadRequestKeyError:
            page = 1
            limit = 5
            # If limit is greater than 100 default to 100
        if limit > 100:
            limit = 100

        try:
            # `q` specifies the search term
            # the "search bucketlist by name" parameter
            q = request.args['q']
        except BadRequestKeyError:
            q = ''

        try:
            bucketlst = (models.Bucketlist).query.filter(
                models.Bucketlist.created_by == current_user.id,
                models.Bucketlist.name.like('%' + q + '%')).paginate(page, limit)

        except SQLAlchemyError:
            return {'message': 'Error'}


        current_url = request.url
        next_url, prev_url = "", ""
        base_url = str(current_url[0:current_url.rindex('/')])
        if bucketlst.has_next:
            next_page = bucketlst.next_num
            items = bucketlst.per_page
            next_url ="{}?page={}&limit={}".format(base_url,str(next_page), str(items))

        if bucketlst.has_prev:
            prev_page = bucketlst.prev_num
            items = bucketlst.per_page
            prev_url ="{}?page={}&limit={}".format(base_url,str(prev_page), str(items))

        results = marshal(bucketlst.items, bucketlist_fields)
        info_dict = {}
        # results with paging
        if len(results) > 0:
            info_dict = {"data": results, "paging":
                       {"previous": prev_url, "next": next_url,
                        "pageNum": page, "count": len(bucketlst.items)}}
        return info_dict

    def post(self):
        """
        Create a bucketlist.
        Args:
            self
        Returns:
            The bucketlist created.
        """
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        current_date = time.strftime('%Y/%m/%d %H:%M:%S')

        try:
            bucketlst = models.Bucketlist(
                name=args.name, date_created=current_date,
                date_modified=current_date, created_by=int(current_user.id))
            db.session.add(bucketlst)
            db.session.commit()
            return marshal(bucketlst, bucketlist_fields)

        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error creating bucketlist'}


class BucketlistResource(Resource):
    """
    Resource that handles actions on a single bucketlist.
    Url:
        '/bucketlists/<id>'
    Methods:
        'GET', 'DELETE','PUT'"""

    decorators = [login_required]

    def get(self, id):
        """
         Query one bucketlist by ID.
        Args:
            self
            id: The bucketlist id
        Returns:
            The required bucketlist details.
        Raises:
            Error."""
        try:
            bucketlst = db.session.query(models.Bucketlist).filter_by(
                id=id, created_by=current_user.id).one()
            return marshal(bucketlst, bucketlist_fields)
        except SQLAlchemyError:
            return {'message': 'No Result'}, 400

    def put(self, id):
        """Update the bucketlist specified by id.
        Args:
            self
            id: ID of the bucketlist to be updated.
        Returns:
            The updated bucketlist details.
        Raises:
            Error.
        """
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()

        try:
            bl = db.session.query(models.Bucketlist).filter_by(
                id=id, created_by=current_user.id).one()
            bl.name = args.name
            bl.date_modified = time.strftime('%Y/%m/%d %H:%M:%S')
            db.session.commit()
            return marshal(bl, bucketlist_fields)
        except NoResultFound:
            db.session.rollback()
        return {'message': 'Error Updating'}

    def delete(self, id):
        """
        Delete a bucketlist specified by id.
        Args:
            self
            id: ID of bucketlist to be deleted.
        Returns:
            A message on successful delete operation.
        Raises:
            Error.
        """
        try:
            bq = db.session.query(models.Bucketlist).filter_by(
                id=id, created_by=current_user.id).one()
            db.session.delete(bq)
            db.session.commit()
            if bq:
                return {'message': 'Sucessfully Deleted'}
        except NoResultFound:
            db.session.rollback()
        return {'message': 'Error Deleting'}


class BucketlistItem(Resource):
    """
    Resource that handles actions on bucketlist items.
    Url:
        '/bucketlists/<id>/items/<item_id>'
    Methods:
       'GET', 'PUT', 'DEL'
    """

    decorators = [login_required]

    def get(self, id, item_id):
        """Show an item from bucketlist `id` specified by `item_id`."""
        try:
            bqi = db.session.query(models.Item).filter_by(
                bucketlist_id=id, id=item_id).one()
            return marshal(bqi, bucketlist_item_fields)
        except NoResultFound:
            return {'message': 'No Result'}, 404

    def put(self, id, item_id):
        """Edit an item from bucketlist `id` specified by `item_id`."""
        parser = RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('done')
        args = parser.parse_args()

        try:
            bli = db.session.query(models.Item).filter_by(
                bucketlist_id=id, id=item_id).one()
            bli.date_modified = time.strftime('%Y/%m/%d %H:%M:%S')
            if args.name:
                bli.name = args.name
            if args.done:
                bli.done = args.done
            db.session.commit()
            return marshal(bli, bucketlist_item_fields)
        except NoResultFound:
            db.session.rollback()
        return {'message': 'Error Updating'}, 400

    def delete(self, id, item_id):
        """Delete an item from bucketlist `id` specified by `item_id`."""
        try:
            bqi = db.session.query(models.Item).filter_by(
                bucketlist_id=id, id=item_id).one()
            db.session.delete(bqi)
            db.session.commit()
            if bqi:
                return {'message': 'Item deleted'}
        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error Deleting item'}


class BucketlistItems(Resource):
    """
    Resource for creating bucketlist items
    Endpoint:
        '/bucketlists/<id>/items/'
    Methods:
        'POST'
    """

    decorators = [login_required]

    def post(self, id):
        """
        Adds an item to specified bucketlist `id`.
        Args:
            self
            id: ID of the bucketlist item is to be created in.
        Returns:
            The updated bucketlist showing the new item added.
        Raises:
             Error
        """
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('done')
        args = parser.parse_args()

        current_date = time.strftime('%Y/%m/%d %H:%M:%S')

        try:
            bli = models.Item(
                name=args.name, date_created=current_date,
                date_modified=current_date, done=args.done, bucketlist_id=id)
            db.session.add(bli)
            db.session.commit()
            return marshal(bli, bucketlist_item_fields)
        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error creating bucketlist'}


class UserResource(Resource):
    """Resource for adding users."""

    def post(self):
        """Add(register) a user."""
        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        user = models.User(username=args.username, email=args.email)
        user.hash_password(args.password)
        try:
            db.session.add(user)
            db.session.commit()
            return {'message': 'user created'}
        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error creating user'}
