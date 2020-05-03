import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'garytse17', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
   
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """ Test get_categories() on empty table"""

        res = self.client().get('/categories')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 6)
        self.assertEqual(data['1'], 'Science')
        self.assertEqual(data['6'], 'Sports')

    def test_get_questions(self):
        """
            Test get_questions() for all questions
        """

        res = self.client().get('/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)

    def test_get_questions_by_category(self):
        """
            Test get_category_questions() by category
        """

        res = self.client().get('/questions?category=3')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['total_questions'], 3)

    def test_404_for_questions_category_out_of_range(self):

        """
            Test get_questions() for non-existent category
        """

        res = self.client().get('/questions?category=8')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_for_category_questions_category_out_of_range(self):
        """
            Test get_category_questions() for non-existent category
        """

        res = self.client().get('/category/8/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_for_questions_page_out_of_range(self):
        """
            Test get_questions() for page out of range
        """

        res = self.client().get('/questions?page=10')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        """
            Test search_question() for existing question
        """

        res = self.client().post('/questions/search', json={'searchTerm': 'taj'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['questions'][0]['id'], 15)
        self.assertEqual(data['total_questions'], 1)

    def test_search_question_for_nonexistent_question(self):
        """
            Test search_question() for non-existent question
        """

        res = self.client().post('/questions/search', json={'searchTerm': 'marco polo'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)

    def test_422_for_search_question(self):
        """
            Test search_question() for invalid query 
        """
        res = self.client().post('/questions/search', json={'search_term': 'taj'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_question(self):
        """
            Test create_question()
        """
        res = self.client().post('/questions', json={
            'question': 'Where is Manchester United from?',
            'answer': 'UK',
            'difficulty': '1',
            'category': '6'
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_for_create_question(self):

        """
            Test create_question() for insufficient input
        """
        res = self.client().post('/questions', json={
            'question': 'Where is Liverpool from?',
            'answer': 'UK',
            'difficulty': '1',
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        """
            Test delete_question()
        """

        res = self.client().delete('/questions/24')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_question(self):
        """
            Test delete_question() for nonexistent question
        """

        res = self.client().delete('/questions/30')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_play_quiz(self):
        """
            Test play_quiz()
        """

        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 5}
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 5)

    def test_play_quiz_no_remaining_questions(self):
        """
            Test play_quiz() where there are no remaining questions in category
        """

        res = self.client().post('/quizzes', json={
            'previous_questions': [20,21,22],
            'quiz_category': {'id': 1}
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)

    def test_422_play_quiz_nonexistent_category(self):
        """
            Test play_quiz() where category does not exist
        """

        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 10}
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()