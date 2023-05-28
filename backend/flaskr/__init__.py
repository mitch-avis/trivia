from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import Category, Question, setup_db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    if test_config is not None:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="postgresql://postgres@localhost:5432/trivia"
        )

    setup_db(app)
    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app)

    @app.after_request
    def after_request(response):
        """Sets Access-Control-Allow Headers and Methods."""
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route("/categories")
    def get_categories():
        """Gets all available categories."""
        selection = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection:
            categories[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify({"success": True, "categories": categories})

    @app.route("/questions")
    def get_questions():
        """Gets a paginated list of questions, number of total questions, current category, and all
        categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
        """
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        selection = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection:
            categories[category.id] = category.type

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories,
                "current_category": "History",
            }
        )

    @app.route("/questions", methods=["POST"])
    def create_question():
        """Creates a new question, which requires the question and answer text, difficulty score,
        and category."""
        try:
            body = request.get_json()
            question = body.get("question", None)
            answer = body.get("answer", None)
            difficulty = body.get("difficulty", None)
            category = body.get("category", None)

            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category,
            )
            new_question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": new_question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except Exception:
            abort(422)

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        """Gets questions based on a search term. Returns any questions for whom the search term is
        a substring of the question."""
        body = request.get_json()
        try:
            search = body.get("searchTerm", None)
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            )
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection.all()),
                    "current_category": "History",
                }
            )
        except Exception:
            abort(422)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """Deletes a question using a question ID."""
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except Exception:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(415)
    def unsupported_media_type(error):
        return (
            jsonify({"success": False, "error": 415, "message": "unsupported media type"}),
            415,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app
