import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import storage
from web import app


class WebApiTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_tasks_file = storage.TASKS_FILE
        storage.TASKS_FILE = Path(self.temp_dir.name) / "tasks.json"
        self.client = TestClient(app)

    def tearDown(self):
        storage.TASKS_FILE = self.original_tasks_file
        self.temp_dir.cleanup()

    def test_show_page_returns_html(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Трекер задач", response.text)

    def test_get_tasks_returns_empty_list_by_default(self):
        response = self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_task_saves_new_task(self):
        response = self.client.post("/api/tasks", json={"title": " Learn FastAPI "})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            [{"id": 1, "title": "Learn FastAPI", "done": False}],
        )

    def test_create_task_rejects_empty_title(self):
        response = self.client.post("/api/tasks", json={"title": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Task title is required")

    def test_complete_task_marks_task_done(self):
        self.client.post("/api/tasks", json={"title": "Write tests"})

        response = self.client.post("/api/tasks/1/done")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "title": "Write tests", "done": True}],
        )

    def test_complete_task_returns_404_for_missing_task(self):
        response = self.client.post("/api/tasks/404/done")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Task not found")

    def test_update_task_changes_task_title(self):
        self.client.post("/api/tasks", json={"title": "Old title"})

        response = self.client.patch("/api/tasks/1", json={"title": " New title "})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [{"id": 1, "title": "New title", "done": False}],
        )

    def test_update_task_rejects_empty_title(self):
        self.client.post("/api/tasks", json={"title": "Old title"})

        response = self.client.patch("/api/tasks/1", json={"title": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Task title is required")

    def test_update_task_returns_404_for_missing_task(self):
        response = self.client.patch("/api/tasks/404", json={"title": "New title"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Task not found")

    def test_delete_task_removes_task(self):
        self.client.post("/api/tasks", json={"title": "Delete me"})

        response = self.client.delete("/api/tasks/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_delete_task_returns_404_for_missing_task(self):
        response = self.client.delete("/api/tasks/404")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Task not found")


if __name__ == "__main__":
    unittest.main()
