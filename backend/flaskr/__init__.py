import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "trivia")
DB_PATH = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

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
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(SQLALCHEMY_DATABASE_URI=DB_PATH)
    from models import Category, Question, db  # noqa: E0402

    db.init_app(app)
    with app.app_context():
        db.create_all()
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
        """Gets a paginated list of questions, number of total questions, all categories, and
        current category."""
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
        """Gets questions based on a search term. Returns any questions for which the search term is
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
        current_category = db.session.get(Category, current_category_id).type
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": total_questions,
                "current_category": current_category,
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

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        """Gets questions to play the quiz. Takes category and previous question parameters and
        returns a random question within the given category, if provided, and that is not one of the
        previous questions."""
        # Get request parameters
        body = request.get_json()
        previous_questions = body.get("previous_questions", [])
        # Get quiz category if passed in, else default to 0 for ALL
        quiz_category = body.get("quiz_category", {"id": "0"})
        category_id = int(quiz_category.get("id", 0))
        # Get questions from ALL categories
        if category_id == 0:
            results = db.session.query(Question).order_by(Question.id).all()
        # Get questions from specific category using category_id
        else:
            results = (
                db.session.query(Question)
                .join(Category, Question.category == category_id)
                .order_by(Question.id)
                .all()
            )
        # Get all available question IDs
        question_ids = [question.id for question in results]
        # Remove previous question IDs from list of available question IDs
        for question_id in previous_questions:
            if question_id in question_ids:
                question_ids.remove(question_id)
        # If question list is not empty, get a random one to return
        if question_ids:
            random_question_id = random.choice(question_ids)
            random_question = db.session.get(Question, random_question_id).format()
        # Else, return none (end of game)
        else:
            random_question = None
        return jsonify(
            {
                "success": True,
                "question": random_question,
            }
        )

    # Error handlers for all expected errors, including 404 and 422.
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
