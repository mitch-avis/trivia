# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in
   the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

2. **Virtual Environment** - It is recommended to work within a virtual environment whenever using
   Python for projects. This keeps your dependencies for each project separate and organized.
   Instructions for setting up a virual environment for your platform can be found in the
   [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required
   dependencies by navigating to the `/backend` directory and running:

   ```bash
   pip install -r requirements.txt
   ```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is
  required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the
  lightweight SQL database. You'll primarily work in `__init__.py` and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle
  cross-origin requests from the frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder, run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` folder, first ensure you are working using your created virtual
environment.

To run the server, first set the flask environment variables:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=true
```

Then, execute:

```bash
flask run
```

## Testing

To initialize the test database, navigate to the backend folder and run the following commands:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

To run the tests:

```bash
python test_flaskr.py
```

Optionally, pytest can be run directly for prettier formatting and to display code coverage:

```bash
pytest --cov-report term-missing --cov=flaskr test_flaskr.py
```

## API Reference

### Getting Started

- Base URL: At present, this app can only be run locally and is not hosted as a base URL. The
  backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the
  frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```

The API will return six error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 415: Unsupported Media Type
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints

#### {GET} /categories

- Description:
  - Gets all available categories
- Request Arguments:
  - None
- Returns:
  - A dictionary object with two keys:
    - `success` {bool}: Success value
    - `categories` {dict}: A dictionary containing `id: category_string` key:value pairs
- Example Request:

```bash
curl http://127.0.0.1:5000/categories
```
  
- Example Response:

```json
{
    "success": true,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }
}
```

#### {GET} /questions

- Description:
  - Gets a paginated list of questions, number of total questions, all categories, and current
    category
- Request Arguments:
  - (optional) `page` {int}: Specify which page of questions to return
- Returns:
  - A dictionary object with five keys:
    - `success` {bool}: Success value
    - `questions` {list}: A paginated list of question objects
    - `total_questions` {int}: The total number of questions in the database
    - `categories` {dict}: A dictionary containing `id: category_string` key:value pairs
    - `current_category` {string}: The current category
- Example Request:

```bash
curl http://127.0.0.1:5000/questions?page=2
```
  
- Example Response:

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "total_questions": 19,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science"
}
```

#### {GET} /categories/<category_id>/questions

- Description:
  - Gets a paginated list of questions based on category
- Request Arguments:
  - `category_id` {int}: The ID of the category from which to get questions
  - (optional) `page` {int}: Specify which page of questions to return
- Returns:
  - A dictionary object with four keys:
    - `success` {bool}: Success value
    - `questions` {list}: A paginated list of question objects
    - `total_questions` {int}: The total number of questions in the database
    - `current_category` {string}: The current category
- Example Request:

```bash
curl http://127.0.0.1:5000/category/1/questions
```
  
- Example Response:

```json
{
    "success": true,
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "total_questions": 3,
    "current_category": "Science"
}
```

#### {POST} /questions

- Description:
  - Creates a new question, which requires the question and answer text, difficulty score, and
    category
- Request Arguments:
  - A dictionary object containing four key:value pairs:
    - `question` {string}: Question text
    - `answer` {string}: Answer text
    - `difficulty` {int}: Difficulty score
    - `category` {int}: Category ID
  - (optional) `page` {int}: Specify which page of questions to return
- Returns:
  - A dictionary object with four keys:
    - `success` {bool}: Success value
    - `created` {int}: The question ID of the newly created question
    - `questions` {list}: A paginated list of question objects
    - `total_questions` {int}: The total number of questions in the database
- Example Request:

```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/questions?page=2 -d '{"question":"Who played the role of Scrooge in A Muppet's Christmas Carol?","answer":"Michael Caine","difficulty":"3","category":"5"}'
```
  
- Example Response:

```json
{
    "success": true,
    "created": 40,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "Michael Caine",
            "category": 5,
            "difficulty": 3,
            "id": 40,
            "question": "Who played the role of Scrooge in A Muppet's Christmas Carol?"
        }
    ],
    "total_questions": 20
}
```

#### {POST} /questions/search

- Description:
  - Gets questions based on a search term. Returns any questions for which the search term is a
    substring of the question
- Request Arguments:
  - A dictionary object containing one key:value pair:
    - `searchTerm` {string}: Term to search for
- Returns:
  - A dictionary containing four keys:
    - `success` {bool}: Success value
    - `questions` {list}: A paginated list of question objects matching the search term
    - `total_questions` {int}: The number of questions matching the search term
    - `current_category` {string}: The current category
- Example Request:

```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/questions/search -d '{"searchTerm":"Scrooge"}'
```
  
- Example Response:

```json
{
    "success": true,
    "questions": [
        {
            "answer": "Michael Caine",
            "category": 5,
            "difficulty": 3,
            "id": 41,
            "question": "Who played the role of Scrooge in A Muppet's Christmas Carol?"
        }
    ],
    "total_questions": 1,
    "current_category": "Science"
}
```

#### {DELETE} /questions/<question_id>

- Description:
  - Deletes a question using a question ID
- Request Arguments:
  - `question_id` {int}: The ID of the question to delete
  - (optional) `page` {int}: Specify which page of questions to return
- Returns:
  - A dictionary containing four keys:
    - `success` {bool}: Success value
    - `deleted` {int}: The ID of the question that was deleted
    - `questions` {list}: A paginated list of question objects
    - `total_questions` {int}: The total number of questions in the database
- Example Request:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/41?page=2
```
  
- Example Response:

```json
{
    "success": true,
    "deleted": 41,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        }
    ],
    "total_questions": 19
}
```

#### {POST} /quizzes

- Description:
  - Gets questions to play the quiz. Takes category and previous question parameters and returns a
    random question within the given category, if provided, and that is not one of the previous
    questions
- Request Arguments:
  - (optional) A dictionary object containing two key:value pairs:
    - `quiz_category` {dict}: A dictionary object containing two key:value pairs:
      - `id` {int}: Category ID
      - `type` {string}: Category name
    - `previous_questions` {list}: A list of integers corresponding to the IDs of questions that
      have already been asked
- Returns:
  - A dictionary containing two keys:
    - `success` {bool}: Success value
    - `question` {Question}: A random Question object, which contains five key:value pairs:
      - `id` {int}: Question ID
      - `question` {string}: Question text
      - `answer` {string}: Answer text
      - `category` {int}: Category ID
      - `difficulty` {int}: Difficulty rating
- Example Request:

```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes -d '{"quiz_category":{"id":"1","type":"Science"},"previous_questions":[20,21]}'
```
  
- Example Response:

```json
{
    "success": true,
    "question": {
        "id": 21,
        "question": "Who discovered penicillin?",
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3
    }
}
```

## Deployment

N/A

## Authors

Udacity

Mitch Avis

## Acknowledgements

The awesome team at Udacity.
