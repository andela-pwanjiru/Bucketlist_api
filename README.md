[![Build Status](https://travis-ci.org/andela-pwanjiru/Bucketlist_api.svg?branch=develop)](https://travis-ci.org/andela-pwanjiru/Bucketlist_api)
[![Coverage Status](https://coveralls.io/repos/github/andela-pwanjiru/Bucketlist_api/badge.svg?branch=develop)](https://coveralls.io/github/andela-pwanjiru/Bucketlist_api?branch=develop)
# Bucketlist API
This bucketlist API built on flask.

# Features:

*  A user can log in.
*  A user is authenticated.
*  Create new bucketlist items.
*  Update and delete the items.
*  Retrieve a list of all created bucket lists by a registered user.
*  Pagination - You can specify the number of results you wish to have returned.
*  Search - get a particular bucketlist.

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
`python api.py`


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

To paginate :
* **`/bucketlists?page=""&limit=""`**
    * GET - List bucketlist according to the limit specified.

To search :
* **`/bucketlists?q=""`**
    * GET - List the searched bucketlist       



## Testing
To run tests:
`nosetests`
