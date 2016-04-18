
# Bucketlist API
This bucketlist API built on flask.

# Features:

1. A user can log in.
2. A user is authenticated.
3. Create new bucketlist items.
4. Update and delete the items.
5. Retrieve a list of all created bucket lists by a registered user.
6 .Pagination - You can specify the number of results you wish to have returned.
7 .Search - get a particular bucketlist.

## Usage:

* Clone the repo: git@github.com:andela-pwanjiru/Bucketlist_api.git
* Install requirements.
 `pip install -r requirements.txt`

* Perform database migrations.
```
python manage.py db init
python manage.py db migrate
```

* Run the application
`python authentication.py`


## EndPoints
Access to all endpoints except login and registration require authentication.
The login endpoint returns a token which should be added to the headers on
all other requests. The header should be given the name `token`

* **`/auth/register`**
    * POST - Creates/registers a user

* **`/auth/login`**
    * POST - Logs a user in.

* **`/bucketlists/`**
    * POST - Create a new bucket list
    * GET - List all the created bucket lists

* **`/bucketlists/<id>`**
    * DELETE - Delete a given bucket list (Identified by <id>)
    * GET - Get single bucket list  (Identified by <id>)
    * PUT - Update a given bucket list  (Identified by <id>)


* **`/bucketlists/<id>/items/`**
    * POST - Create a new item in bucket list

* **`/bucketlists/<id>/items/<item_id>`**
    * PUT - Update a bucket list item
    * DELETE - Delete an item from a bucket list



## Testing
Tests are run from the root folder
`nosetests`
To include Coverage in the tests
`nosetests --with-coverage --cover-package=.`
