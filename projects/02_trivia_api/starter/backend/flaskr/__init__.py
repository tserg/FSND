import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():

    try:

      categories = Category.query.distinct('type').all()

      formatted_categories = {}

      for category in categories:

        formatted_categories[category.id] = category.type
      
      return jsonify(formatted_categories)


    except:

      abort(404)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def get_questions():

    try:

      page = request.args.get('page', 1, type=int)
      category = request.args.get('category', 0, type=int)

      start = (page-1)*10
      end = start + QUESTIONS_PER_PAGE

      # extract questions based on category

      if category == 0:

        questions = Question.query.all()

      else: 

        questions = Question.query.filter(Question.category == category).all()

      formatted_questions = [question.format() for question in questions]

      categories = Category.query.all()

      formatted_categories = [category.type for category in categories]

      questions_count = len(questions)

      # check if page count exceeds question count

      if start+1 <= questions_count:

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': category
            
          })

      else:

        abort(404)

    except:

      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:

      question = Question.query.get(question_id)

      question.delete()

      return jsonify({
        'success': True
      })

    except:

      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():

    try:

      question = request.get_json()['question']
      answer = request.get_json()['answer']
      difficulty = request.get_json()['difficulty']
      category = request.get_json()['category']

      if question == None or answer == None or difficulty == None or category == None:
        abort(400)

      new_question = Question(
          question = question,
          answer = answer,
          difficulty = difficulty,
          category = category
        )

      new_question.insert()

      return jsonify({
          'success': True
        })

    except:

      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    try:

      search_term = request.get_json()['searchTerm']

      print(search_term)

      results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()

      formatted_results = [question.format() for question in results]

      if formatted_results == []:

        return jsonify({
            'questions': [],
            'total_questions': 0,
            'current_category': []
          })

      else:
        return jsonify({
            'questions': formatted_results,
            'total_questions': len(formatted_results),
            'current_category': [(question['category']) for question in formatted_results]
          })

    except:

      abort(422)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category_questions(category_id):

    try:

      questions = Question.query.filter(Question.category == category_id).all()

      formatted_questions = [question.format() for question in questions]

      return jsonify({
          'questions': formatted_questions,
          'total_questions': len(formatted_questions),
          'current_category': category_id
        })

    except:

      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
      })

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):

    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
      }), 500

  @app.errorhandler(503)
  def service_unavailable(error):

    return jsonify({
        'success': False,
        'error': 503,
        'message': 'service unavailable'
      }), 503


  
  return app

    