import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.storage import database


class TaskApiTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_tasks_file = database.TASKS_FILE
        database.TASKS_FILE = Path(self.temp_dir.name) / "tasks.json"
        self.client = TestClient(app)

    def tearDown(self):
        database.TASKS_FILE = self.original_tasks_file
        self.temp_dir.cleanup()

    def test_create_task(self):
        response = self.client.post("/api/tasks", json={"title": "Купить хлеб"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Купить хлеб", "done": False},
        )

    def test_index_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Трекер задач", response.text)

    def test_get_tasks_list(self):
        self.client.post("/api/tasks", json={"title": "Первая"})
        self.client.post("/api/tasks", json={"title": "Вторая"})

        response = self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {"id": 1, "title": "Первая", "done": False},
                {"id": 2, "title": "Вторая", "done": False},
            ],
        )

    def test_update_task(self):
        self.client.post("/api/tasks", json={"title": "Старое название"})

        response = self.client.patch(
            "/api/tasks/1",
            json={"title": "Новое название", "done": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Новое название", "done": True},
        )

    def test_mark_task_done(self):
        self.client.post("/api/tasks", json={"title": "Купить хлеб"})

        response = self.client.patch("/api/tasks/1/done")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Купить хлеб", "done": True},
        )

    def test_delete_task(self):
        self.client.post("/api/tasks", json={"title": "Первая"})
        self.client.post("/api/tasks", json={"title": "Вторая"})

        response = self.client.delete("/api/tasks/1")
        tasks_response = self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            tasks_response.json(),
            [{"id": 2, "title": "Вторая", "done": False}],
        )

    def test_missing_task_returns_404(self):
        response = self.client.patch("/api/tasks/999", json={"title": "Нет задачи"})

        self.assertEqual(response.status_code, 404)

    def test_empty_title_returns_validation_error(self):
        response = self.client.post("/api/tasks", json={"title": "   "})

        self.assertEqual(response.status_code, 422)

    def test_created_ids_are_stable_after_delete(self):
        self.client.post("/api/tasks", json={"title": "Первая"})
        self.client.post("/api/tasks", json={"title": "Вторая"})
        self.client.delete("/api/tasks/1")

        response = self.client.post("/api/tasks", json={"title": "Третья"})

        self.assertEqual(response.json()["id"], 3)


if __name__ == "__main__":
    unittest.main()
