from flask.ext.testing import TestCase
from ..api import app, db
from ..config import TestingConfig


class BaseTestCase(TestCase):
    """A base test case for User and Bucketlist test classes."""

    def create_app(self):
        """Set up the test test_client. Returns an `app` instance."""
        # set up cofig options
        app.config.from_object(TestingConfig)
        self.client = app.test_client()
        return app

    def setUp(self):
        """Run instructions before the each test is executed."""
        db.create_all()
        self.create_user = self.client.post('/auth/register', data=dict(
            username='username', password='password', email='email@email.com'))
        get_token = self.client.post('/auth/login', data=dict(
            username='username', password='password'))
        self.token = get_token.json['token']
        self.bucketlst1 = self.client.post('/bucketlists/', data=dict(
            name='First Bucketlist'), headers={'token': self.token})
        self.bucketlst2 = self.client.post('/bucketlists/', data=dict(
            name='Second Bucketlist'), headers={'token': self.token})

        self.bucketlistitem1 = self.client.post(
            '/bucketlists/{0}/items/'.format(self.bucketlistitem1.json['id']),
            data=dict(name='First Bucketlist Item Name', done='0'),
            headers={'token': self.token})
        self.bucketlistitem2 = self.client.post(
            '/bucketlists/{0}/items/'.format(self.bucketlistitem2.json['id']),
            data=dict(name='Second Bucketlist Item Name', done='1'),
            headers={'token': self.token})

        resp = self.client.get('/bucketlists/', headers={'token': self.token})
        self.initial_count = len(resp.json)

        self.exp_token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ1MDY4OTA0MSwiaWF0IjoxND\
        UwNjg4NDQxfQ.WyIxIiwiJDYkcm91bmRzPTY0Mjg1NyRGcUZsSUxBeDh6UEhPWDNhJDd2L0\
        5tUy9TajhKQVRSRVRGaUlYZVhjaE9aZ0JLbDVTREh3czg1LkhBT20xNi9BTW9kSFluZlhmM\
        zk5MXFWWVpDclNsVzRBcHkuSTdFdlAuOWtEQncvIl0.IPzsof8lZr1vGPgxG-pDUo7RO5nO\
        aLKkXaa-lIs0c_4'

        self.invalid_token = 'eqwJhbGciOiIUzI1NiIsImV4cCI6MTQ1MDY4OTA0MSwiaWF0IjoxND\
        UwNjg4NDQxfQ.WyIxIiwiJDY98w1bmRzPTY0Mjg1NyRGcUZsSUxBeDh6UEhPWDNhJDd2L0\
        5tUy9TajhKQVRSRVRGaUlYZVhjaE9aZ0JLbDVTREh3czg1LkhBT20xNi9BTW9kSFluZlhmM\
        zk5MXFWWVpDclNsVzRBcHkuSTdFdlAuOWtEQncvIl0.IPzsof8lZr1vGPgxG-pDUo7RO5nO\
        aLKkXaa-lIs0c_4'

    def tearDown(self):
        """Destroy test db at end of tests."""
        db.session.remove()
        db.drop_all()
