import json
import unittest

from flaskr import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(
            test_config={
                "SQLALCHEMY_DATABASE_URI": "postgresql://postgres@localhost:5432/trivia_test",
            }
        )
        self.client = self.app.test_client
        self.new_question = {
            "question": "Who played the role of Scrooge in A Muppet's Christmas Carol?",
            "answer": "Michael Caine",
            "difficulty": 3,
            "category": 5,
        }
        self.empty_question = {
            "question": "",
            "answer": "",
            "difficulty": 1,
            "category": 1,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_1_get_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data["categories"]))

    def test_2_get_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 10)
        self.assertEqual(data["total_questions"], 19)
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    def test_3_get_questions_404_invalid_page(self):
        response = self.client().get("/questions?page=1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")

    def test_4_create_new_question(self):
        response = self.client().post("/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])
        self.assertEqual(len(data["questions"]), 10)
        self.assertEqual(data["total_questions"], 20)

    def test_4_create_new_question_invalid_values(self):
        response = self.client().post("/questions", json=self.empty_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_5_search_questions_with_results(self):
        response = self.client().post("/questions/search", json={"searchTerm": "Scrooge"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["total_questions"], 1)
        self.assertTrue(data["current_category"])

    def test_6_delete_question(self):
        # First get the question_id of newly created book to delete it
        search_response = self.client().post("/questions/search", json={"searchTerm": "Scrooge"})
        search_data = json.loads(search_response.data)
        question_id = search_data["questions"][0]["id"]

        delete_response = self.client().delete(f"/questions/{question_id}")
        delete_data = json.loads(delete_response.data)

        self.assertEqual(delete_response.status_code, 200)
        self.assertTrue(delete_data["success"])
        self.assertEqual(delete_data["deleted"], question_id)
        self.assertTrue(delete_data["questions"])
        self.assertTrue(delete_data["total_questions"])

    def test_7_delete_nonexistent_question(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "unprocessable")

    def test_8_search_questions_without_results(self):
        response = self.client().post("/questions/search", json={"searchTerm": "Scrooge"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 0)
        self.assertEqual(data["total_questions"], 0)
        self.assertTrue(data["current_category"])

    def test_9_get_questions_by_category(self):
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(len(data["questions"]), 3)
        self.assertEqual(data["total_questions"], 3)
        self.assertEqual(data["current_category"], "Science")

    def test_10_play_quiz_all_categories(self):
        response = self.client().post("/quizzes", json={})
        data = json.loads(response.data)
        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["question"]))

    def test_10_play_quiz_specific_categories(self):
        response = self.client().post(
            "/quizzes",
            json={"quiz_category": {"type": "Science", "id": "1"}, "previous_questions": [20, 21]},
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["question"]))
        self.assertEqual(data["question"]["id"], 22)

    def test_10_play_quiz_no_questions_left(self):
        response = self.client().post(
            "/quizzes",
            json={
                "quiz_category": {"type": "Science", "id": "1"},
                "previous_questions": [20, 21, 22],
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["question"], None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
