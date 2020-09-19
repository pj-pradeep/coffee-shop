import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    all_drinks = Drink.query.all()
    if all_drinks is None or len(all_drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in all_drinks]
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    all_drinks = Drink.query.all()
    if all_drinks is None or len(all_drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in all_drinks]
    }), 200



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    request_body = request.get_json()

    if not request_body:
        print('There was no request body. Not a valid request')
        abort(400)

    title = request_body.get('title', None)
    recipe = request_body.get('recipe', None)

    if (title is None or recipe is None):
        print("Request body missing Title or Recipe information required to create a drink")
        abort(422)    

    drink = Drink()
    drink.title = title
    drink.recipe = json.dumps([recipe])
    
    drink.insert()

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    drink = Drink.query.get(id)

    if drink is None:
        print(f'There is no drink with id {drink_id}. Nothing to update')
        abort(404)

    request_body = request.get_json()

    if not request_body:
        print('There was no request body. Not a valid request')
        abort(400)

    title = request_body.get('title', None)
    recipe = request_body.get('recipe', None)

    try:
        if title:
            drink.title = title        
        
        if recipe:
            drink.recipe = json.dumps([recipe])

        drink.update()
        
    except Exception as e:
        print(f'There was an exception trying to update drink {id}')
        abort(422)

    return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })  


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)

    if drink is None:
        print(f'There is no drink with id {drink_id}. Nothing to update')
        abort(404)

    try:
        drink.delete()
    except Exception as e:
        print(f'There was an exception trying to delete drink {id}')
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    })



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource Not Found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "code": ex.error['code'],
        "description": ex.error['description']
    }), ex.status_code