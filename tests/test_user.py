import unittest
from tests import BaseTestCase


class TestUser(BaseTestCase):
    """Test user functions."""

    def test_wrong_login(self):
        """Test login failure with wrong credentials.

        With wrong login credentials a token should not be returned. A `Login
        Failed` message should be returned
        """
        failed = self.client.post('/auth/login', data=dict(
            username='username', password='pass'))
        self.assertNotIn('token', failed.json)
        self.assertIn('message', failed.json)
        self.assertEqual(failed.json['message'], 'Login Failed')

    def test_user_registration(self):
        """Test registration failure with no data provided.

        To create a user a username, password and email address are required.

        """
        no_email = self.client.post('/auth/register', data=dict(
            username='username', password='password'))
        no_password = self.client.post('/auth/register', data=dict(
            username='username', email='email@email.com'))
        no_username = self.client.post('/auth/register', data=dict(
            password='password', email='email@email.com'))
        self.assert_400(no_email)
        self.assert_400(no_password)
        self.assert_400(no_username)

    def test_user_creation_unique_fields(self):
        """Test registration failure with fields already existing in DB.

        To create a user a username, password and email address are required
        """
        failed = self.client.post('/auth/register', data=dict(
            username='username', password='password', email='email@email.com'))
        self.assertEqual(
            failed.json['message'], 'Error creating user')


if __name__ == '__main__':
    unittest.main()