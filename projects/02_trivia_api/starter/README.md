# Full Stack Trivia Project

This is a trivia app for Udacity's Full Stack Nanodegree Programme.

In the trivia app, you will be able to:

1. Display questions - both all questions and by category. Each question will display the following formation: question, answer (with the option to show or hide), category and difficulty rating. 
2. Delete questions.
3) Add questions.
4) Search for questions based on a text query string.
5) Play the quiz game, with questions either randomised as a whole or within a specific category. 

## Getting Started

### Prerequisites & Installation

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

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

##### Key dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

### Local Development

#### Database Setup

First, create the database in your psql terminal

Run:
```
createdb trivia
```

For Windows:
```
CREATE DATABASE trivia;
```

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

For Windows, connect to the database in the psql terminal and run:
```
\c trivia;
\i YOUR_PATH\trivia.psql
```

#### Backend Setup

Add in your username and password for psql in models.py to connect to your local database:
```
database_path = "postgres://{}:{}@{}/{}".format(YOUR_USERNAME, YOUR_PASSWORD, 'localhost:5432', database_name)
```

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

For Windows, navigate to the flaskr directory and execute:

```
set FLASK_APP=__init__.py
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

#### Frontend Setup

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Tests

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

#### For Windows

Run the following in your psql terminal:
```
DROP DATABASE trivia_test;
CREATE DATABASE trivia_test;
\c trivia_test
\i (INSERT YOUR PATH)\trivia.psql
```

Then, navigate to the backend folder in your Python terminal and run:
```
flask run
```

## API Reference

### Getting Started

* Base URL: This app is currently meant to be run locally.
  *The backend app is hosted at `http://127.0.0.1:5000`
  *The frontend app is hosted at `http//127.0.0.1:3000`
* Authentication: This version of the application does not require authenticaation or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 400',
    'message': 'bad request'

}
```

The API will return the following error types when requests fail:
* 400: Bad request
* 404: Resource not found
* 405: Method not allowed
* 422: Unprocessable
* 500: Internal server error
* 503: Service unavailable

### Endpoints

#### GET /categories
* General:
  * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Sample: `curl http://127.0.0.1:5000/categories`

```
{
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
}
```

#### GET /questions
* General
  * Fetches all questions (or by categories if there is a request argument to choose category). If no category is selected, the default value is 0, which fetches all questions.
  * Results are paginated in groups of 10. Include a request argument to choose page number starting from 1.
* Sample: `curl http://127.0.0.1:5000/questions`

```
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "current_category": 0,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bir Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### GET /categories/{category_id}/questions
* General
  * Alternative method to fetch questions by categories
* Sample: `curl http://127.0.0.1:5000/categories/3/questions`

```
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "total_questions": 3
}
```

#### POST /questions
* General
  * Creates a question with the following request arguments: question, answer, difficulty and category
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{ "question": "When did World War 2 begin?", "answer": "1945", "difficulty": "1", "category": "3"}" http://127.0.0.1:5000/questions`

```
{
    'success': true
}
```

#### DELETE /questions/{question_id}
* General
  * Deletes a question based on the question id
* Sample: `curl -X DELETE http://127.0.0.1:5000/questions/26`

```
{
    'successs': true
}
```

#### POST /questions/search
* General
  * Fetches a list of questions containing the search term 
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{ "searchTerm": "title" }" http://127.0.0.1:5000/questions/search` 

```
{
    "current_category": [
    4,
    5
    ],
    "questions": [
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "total_questions": 2
}

```

#### POST /quizzes
* General
  * Fetches a random question from the current category that has not been asked in the current quiz
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{ "previous_questions": ["2", "4"], "quiz_category": {"type": "Entertainment", "id": "5"} }" http://localhost:5000/quizzes`

```
{
    "previous_questions": [2,4],
    "question": {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    "quizCategory": "5",
    "success": true
}
```

## Authors

Gary Tse

## Acknowledgements

Introduction and Getting Started adapted from Udacity's default READMEs.


