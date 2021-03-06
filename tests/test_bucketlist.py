import unittest
from tests import BaseTestCase
from models import Bucketlist, Item


class TestBucketList(BaseTestCase):
    """Class to test bucketlists"""

    def test_authentication(self):
        """Test the method to create a new bucket list requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called \
        `Success Bucketlist Name`
        """
        no_auth = self.client.post('/bucketlists/', data=dict(
            name='Bucketlist Name'))
        success = self.client.post('/bucketlists/', data=dict(
            name='Success Bucketlist Name'), headers={'token': self.token})
        expired_token = self.client.post('/bucketlists/', data=dict(
            name='Expired Bucketlist Name'), headers={'token': self.exp_token})
        invalid_token = self.client.post(
            '/bucketlists/', data=dict(name='Expired Bucketlist Name'),
            headers={'token': self.invalid_token})

        bucketlist = Bucketlist.query.filter_by(
            name='Success Bucketlist Name').one()
        self.assertEqual(bucketlist.name, 'Success Bucketlist Name')
        self.assert_200(success)
        self.assert_401(no_auth)
        self.assert_401(expired_token)
        self.assert_401(invalid_token)

    def test_duplicate_fails(self):
        """Test creating a duplicate bucket list fails.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called
        `Success Bucketlist Name`
        """
        duplicate = self.client.post('/bucketlists/', data=dict(
            name='First Bucketlist'), headers={'token': self.token})
        self.assertEqual(
            duplicate.json['message'], 'Error creating bucketlist')

    def test_get_bucketlists_requires_authentication(self):
        """Test the method to list created bucketlists requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. Since the SetUp function adds test bucketlists the \
        successful response should contain 1 or more items
        """
        bl = Bucketlist.query.all()
        no_auth = self.client.get('/bucketlists/')
        get_bl = self.client.get(
            '/bucketlists/', headers={'token': self.token})
        self.assertGreater(len(bl), 0)
        self.assert_401(no_auth)
        self.assert_200(get_bl)

    def test_get_single_bucketlist_requires_authentication(self):
        """Test the method to get a bucketlist succeeds with authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be\
        returned.
        """
        no_auth = self.client.get(
            '/bucketlists/{0}'.format(self.bl1.json['id']))
        get_bl = self.client.get('/bucketlists/{0}'.format(
            self.bl1.json['id']), headers={'token': self.token})
        not_found = self.client.get(
            '/bucketlists/50', headers={'token': self.token})
        self.assert_401(no_auth)
        self.assert_200(get_bl)
        self.assertEqual(not_found.json['message'], 'No Result')

    def test_update_bucketlists(self):
        """Test the method to update a bucketlist requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Bucketlist table should contain a bucketlist called \
        `Edited Bucketlist Name`
        """
        no_auth = self.client.put(
            '/bucketlists/{0}'.format(self.bl1.json['id']))
        put_bucketlist = self.client.put(
            '/bucketlists/{0}'.format(self.bl1.json['id']),
            data=dict(name='Edited Bucketlist Name'),
            headers={'token': self.token})
        invalid_id = self.client.put('/bucketlists/50', data=dict(
            name='Edited Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(id=self.bl1.json['id']).one()
        self.assertEqual(bl.name, 'Edited Bucketlist Name')
        self.assertEqual(invalid_id.json['message'], 'Error Updating')
        self.assert_401(no_auth)
        self.assert_200(put_bucketlist)

    def test_bucketlist_item_creation(self):
        """Test the method to create a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Item table should contain a bucket called `Success \
        Bucketlist Item Name`
        """
        response = self.client.post(
            '/bucketlists/{0}/items/'.format(self.bl1.json['id']),
            data=dict(name='Bucketlist Item Name', done='0'))
        success_response = self.client.post(
            '/bucketlists/{0}/items/'.format(self.bl1.json['id']),
            data=dict(name='Success Bucketlist Item Name', done='0'),
            headers={'token': self.token})
        bucketlistitem = Item.query.filter_by(
            name='Success Bucketlist Item Name').one()
        self.assertEqual(bucketlistitem.name, 'Success Bucketlist Item Name')
        self.assert_401(response)
        self.assert_200(success_response)

    def test_get_single_bucketlist_item(self):
        """Test the method to get a bucketlist item succeeds with authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned."""
        no_auth = self.client.get('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']))
        get_bl = self.client.get(
            '/bucketlists/{0}/items/{1}'.format(
                self.bl1.json['id'], self.bli1.json['id']),
            headers={'token': self.token})
        not_found = self.client.get(
            '/bucketlists/1/items/50', headers={'token': self.token})
        self.assert_401(no_auth)
        self.assert_200(get_bl)
        self.assertEqual(not_found.json['message'], 'No Result')

    def test_update_bucketlist_item(self):
        """Test the method to update a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response should be \
        returned. The Item table should contain a bucketlist item called \
        `Edited Bucketlist Item Name`
        """
        no_auth = self.client.put('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']))
        put_bl = self.client.put(
            '/bucketlists/{0}/items/{1}'.format(
                self.bl1.json['id'], self.bli1.json['id']),
            data=dict(name='Edited Bucketlist Item Name', done='1'),
            headers={'token': self.token})
        invalid_id = self.client.put(
            '/bucketlists/{0}/items/10'.format(self.bl1.json['id']),
            data=dict(name='Edited Bucketlist Item Name', done='1'),
            headers={'token': self.token})
        bli = Item.query.filter_by(id=self.bli1.json['id']).one()
        self.assertEqual(bli.name, 'Edited Bucketlist Item Name')
        self.assertEqual(invalid_id.json['message'], 'Error Updating')
        self.assert_401(no_auth)
        self.assert_200(put_bl)

    def test_del_bucketlist(self):
        """Test the method to delete a bucketlist item requires authentication.

        If the user is unauthenticated a 401 UNAUTHORIZED response should be \
        returned. With an authentication token a 200 OK response and a \
        Deleted message should be returned. The Item table should contain one \
        entry less from the count before deletion
        """
        count_before = Item.query.all()
        no_auth = self.client.delete('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']))
        del_bl = self.client.delete(
            '/bucketlists/{0}/items/{1}'.format(
                self.bl1.json['id'], self.bli1.json['id']),
            headers={'token': self.token})
        invalid_id = self.client.delete('/bucketlists/{0}/items/50'.format(
            self.bl1.json['id']), headers={'token': self.token})
        count_after = Item.query.all()
        self.assertEqual(del_bl.json['message'], 'Item deleted')
        self.assertEqual(invalid_id.json['message'], 'Error Deleting item')
        self.assertEqual(len(count_after), len(count_before) - 1)
        self.assert_401(no_auth)
        self.assert_200(del_bl)

    def test_get_bucketlist_item_belonging_to_current_user_only(self):
        """ Test the method to get a bucketlist from the current_user only.

            If the user requests for a bucketlist not created by them the\
            should get a no result response message. The user should only\
            be able to access bucketlists belonging to them.
        """
        success_result = self.client.get(
            '/bucketlists/{0}'.format(self.bl6.json['id']),
            headers={'token': self.token2})
        no_result = self.client.get(
            '/bucketlists/{0}'.format(self.bl1.json['id']),
            headers={'token': self.token2})
        no_result1 = self.client.get(
            '/bucketlists/{0}'.format(self.bl6.json['id']),
            headers={'token': self.token})
        self.assert_200(success_result)
        self.assertEqual(success_result.json['name'], 'Sixth Bucketlist')
        self.assertEqual(no_result.json['message'], 'No Result')
        self.assert_400(no_result)
        self.assertEqual(no_result1.json['message'], 'No Result')
        self.assert_400(no_result1)


if __name__ == '__main__':
    unittest.main()
