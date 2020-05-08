import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/')
@requires_auth('get:drinks-detail')
def index(payload):

    print(payload)
    return 'Hello World'


@app.route('/drinks', methods=['GET'])
def get_drinks():

    try:

        all_drinks = Drink.query.all()

        drinks = [drink.short() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except:

        abort(404)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):

    try:

        all_drinks = Drink.query.all()

        drinks = [drink.long() for drink in all_drinks]

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except:

        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):

    try:

        title = request.get_json()['title']
        recipe = request.get_json()['recipe']

        formatted_recipe = json.dumps(recipe)

        new_drink = Drink(
            title=title,
            recipe=formatted_recipe
        )

        new_drink.insert()

        drink = [new_drink.long()]

        return jsonify({
            'success': True,
            'drinks': drink
        })

    except:

        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):

    try:

        print("id: " + str(id))

        current_drink = Drink.query.get(id)

        print(current_drink.title)

        if current_drink is None:

            abort(404)

        print(request.get_json())

        # checks if 'title' exists, otherwise error

        if 'title' in request.get_json()['title']:
            title = request.get_json()['title']
            current_drink.title = title

        # checks if 'recipe' exists, otherwise error

        if 'recipe' in request.get_json():
            recipe = request.get_json()['recipe']
            formatted_recipe = json.dumps(recipe)
            current_drink.recipe = formatted_recipe

        return jsonify({
            'success': True,
            'drinks': [current_drink.long()]
        })

    except:

        abort(400)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):

    try:

        current_drink = Drink.query.get(id)

        if current_drink is None:

            abort(404)

        db.session.delete(current_drink)
        db.session.commit()

        return jsonify({
            'success': True,
            'delete': id
        })

    except:

        abort(400)


# Error Handling
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
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    })


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(error):

    return jsonify({
        'success': False,
        'error': AuthError.status_code,
        'message': AuthError.error['description']
    }), 401
