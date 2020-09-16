# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

The application uses Auth0 for authentication and authorization of the api calls. Set below environment variables. You will be able to find the information in your Auth0 account that was setup. For documentation on setting up Auth0, refer to https://auth0.com/docs/quickstart/spa/react#configure-auth0

```bash
export AUTH0_DOMAIN='your AuthO Domain'
export API_AUDIENCE='your Auth0 audience'
```

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## REST API Reference

### General

* **Base URL** - The application is currently implemented to run locally under the standard port 5000. The API base url http://localhost:5000/
* **Authentication** - The application uses Auth0 for authentication and authorization. Please refer to https://auth0.com/docs/quickstart/spa/react#configure-auth0 for information on setting up and configuring Auth0. The application uses bearer token based authenticating and authorizing approach to give access to the REST api endpoints.

Below are the roles that are configured and their permissions
* Barista - can ```get:drink-details```
* Manager - can perform all actions

### Errors

The Coffee shop applicatoin uses convential HTTP response codes to indicate the success or failure of an API request. In general: Codes in 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Below json response will be returned for any failed API request:

```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}
```

List of errors to expect:


Error Code | Error Message
---------- | -------------
404 | Resource Not Found
400 | Bad Request
422 | Unprocessable Error
405 | method not allowed
401 | Authorization header is expected
401 | Authorization header must be in the format Bearer token
401 | Authorization header must start with Bearer
401 | Operation not allowed. Check your permissions.
401 | Authorization malformed.
401 | token is expired
401 | incorrect claims, please check the audience adn issuer
401 | Unable to parse authentication token.
401 | Unable to find appropriate key


### API Endpoints

Import the postman collection ./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json

The collection has all the api endpoints setup. To test teh end points with Postman:
1. Register 2 users - assign the Barista role to one and Manager role to the other.
2. Sign into each account and make note of the JWT.
3. Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
4. Run the collection and correct any errors.
