from flask import Flask, abort, jsonify, request
from flask_cors import CORS

QUESTIONS_PER_PAGE = 10
current_category_id = 1


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
    from models import Category, Question, db  # noqa: E0402

    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app)

    @app.after_request
    def after_request(response):
        """Sets Access-Control-Allow Headers and Methods."""
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        """Gets all available categories."""
        results = db.session.query(Category).order_by(Category.id).all()
        categories = {}
        for category in results:
            categories[category.id] = category.type
        if len(categories) == 0:
            abort(404)
        return jsonify({"success": True, "categories": categories})

    @app.route("/questions", methods=["GET"])
    def get_questions():
        """Gets a paginated list of questions, number of total questions, current category, and all
        categories."""
        question_results = db.session.query(Question).order_by(Question.id).all()
        total_questions = len(question_results)
        current_questions = paginate_questions(request, question_results)
        if len(current_questions) == 0:
            abort(404)
        category_results = db.session.query(Category).order_by(Category.id).all()
        categories = {}
        for category in category_results:
            categories[category.id] = category.type
        if len(categories) == 0:
            abort(404)
        current_category = db.session.get(Category, current_category_id).type
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "categories": categories,
                "current_category": current_category,
            }
        )

    @app.route("/questions", methods=["POST"])
    def create_question():
        """Creates a new question, which requires the question and answer text, difficulty score,
        and category."""
        body = request.get_json()
        question = body.get("question", "")
        answer = body.get("answer", "")
        difficulty = body.get("difficulty", None)
        category = body.get("category", None)
        # Check required fields for invalid values
        if "" in (question, answer) or None in (category, difficulty):
            abort(422)
        try:
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category,
            )
            db.session.add(new_question)
            db.session.commit()
            new_question_id = new_question.id
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        results = db.session.query(Question).order_by(Question.id).all()
        total_questions = len(results)
        current_questions = paginate_questions(request, results)
        return jsonify(
            {
                "success": True,
                "created": new_question_id,
                "questions": current_questions,
                "total_questions": total_questions,
            }
        )

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        """Gets questions based on a search term. Returns any questions for whom the search term is
        a substring of the question."""
        body = request.get_json()
        search = body.get("searchTerm", None)
        results = (
            db.session.query(Question)
            .order_by(Question.id)
            .filter(Question.question.ilike("%{}%".format(search)))
            .all()
        )
        total_questions = len(results)
        current_questions = paginate_questions(request, results)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "current_category": "History",
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """Deletes a question using a question ID."""
        try:
            db.session.get(Question, question_id).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        results = db.session.query(Question).order_by(Question.id).all()
        total_questions = len(results)
        current_questions = paginate_questions(request, results)
        return jsonify(
            {
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": total_questions,
            }
        )

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        """Gets a paginated list of questions based on category."""
        results = (
            db.session.query(Question)
            .join(Category, Question.category == category_id)
            .order_by(Question.id)
            .all()
        )
        total_questions = len(results)
        current_questions = paginate_questions(request, results)
        current_category_id = category_id
        current_category = db.session.get(Category, current_category_id).type
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "current_category": current_category,
            }
        )

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

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}),
            500,
        )

    return app
