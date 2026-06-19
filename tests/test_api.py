import tempfile
import unittest
from pathlib import Path

from httpx import ASGITransport, AsyncClient

from app.__version__ import __version__
from app.main import app
from app.storage import database


class TaskApiTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_tasks_file = database.TASKS_FILE
        database.TASKS_FILE = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        database.TASKS_FILE = self.original_tasks_file
        self.temp_dir.cleanup()

    async def asyncSetUp(self):
        transport = ASGITransport(app=app)
        self.client = AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_create_task(self):
        response = await self.client.post("/api/tasks", json={"title": "Купить хлеб"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Купить хлеб", "done": False},
        )

    async def test_index_page(self):
        response = await self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Трекер задач", response.text)

    async def test_health(self):
        response = await self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["version"], __version__)

    async def test_get_tasks_list(self):
        await self.client.post("/api/tasks", json={"title": "Первая"})
        await self.client.post("/api/tasks", json={"title": "Вторая"})

        response = await self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {"id": 1, "title": "Первая", "done": False},
                {"id": 2, "title": "Вторая", "done": False},
            ],
        )

    async def test_update_task(self):
        await self.client.post("/api/tasks", json={"title": "Старое название"})

        response = await self.client.patch(
            "/api/tasks/1",
            json={"title": "Новое название", "done": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Новое название", "done": True},
        )

    async def test_mark_task_done(self):
        await self.client.post("/api/tasks", json={"title": "Купить хлеб"})

        response = await self.client.patch("/api/tasks/1/done")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"id": 1, "title": "Купить хлеб", "done": True},
        )

    async def test_delete_task(self):
        await self.client.post("/api/tasks", json={"title": "Первая"})
        await self.client.post("/api/tasks", json={"title": "Вторая"})

        response = await self.client.delete("/api/tasks/1")
        tasks_response = await self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            tasks_response.json(),
            [{"id": 2, "title": "Вторая", "done": False}],
        )

    async def test_missing_task_returns_404(self):
        response = await self.client.patch(
            "/api/tasks/999",
            json={"title": "Нет задачи"},
        )

        self.assertEqual(response.status_code, 404)

    async def test_empty_title_returns_validation_error(self):
        response = await self.client.post("/api/tasks", json={"title": "   "})

        self.assertEqual(response.status_code, 422)

    async def test_created_ids_are_stable_after_delete(self):
        await self.client.post("/api/tasks", json={"title": "Первая"})
        await self.client.post("/api/tasks", json={"title": "Вторая"})
        await self.client.delete("/api/tasks/1")

        response = await self.client.post("/api/tasks", json={"title": "Третья"})

        self.assertEqual(response.json()["id"], 3)


if __name__ == "__main__":
    unittest.main()
