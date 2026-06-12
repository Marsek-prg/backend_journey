import unittest

from app.services.task_service import (
    add_task,
    delete_task,
    get_tasks_text,
    mark_task_done,
    normalize_tasks,
)


class TaskServiceTest(unittest.TestCase):
    def test_add_task_rejects_empty_title(self):
        tasks = []

        result = add_task(tasks, "   ")

        self.assertIsNone(result)
        self.assertEqual(tasks, [])

    def test_add_mark_and_delete_task(self):
        tasks = []

        created_task = add_task(tasks, "Купить хлеб")

        self.assertEqual(created_task, {"id": 1, "title": "Купить хлеб", "done": False})

        updated_task = mark_task_done(tasks, 1)
        self.assertEqual(updated_task, {"id": 1, "title": "Купить хлеб", "done": True})

        self.assertTrue(delete_task(tasks, 1))
        self.assertEqual(tasks, [])

    def test_get_tasks_text_normalizes_tasks(self):
        tasks = [
            {"title": "Первая", "done": False},
            {"title": "Вторая", "done": True},
            {"title": "  "},
            "bad data",
        ]

        lines = get_tasks_text(tasks)

        self.assertEqual(
            lines,
            [
                "1. Первая [Не выполнена]",
                "2. Вторая [Выполнена]",
            ],
        )

    def test_delete_task_keeps_existing_ids_stable(self):
        tasks = [
            {"id": 1, "title": "Первая", "done": False},
            {"id": 5, "title": "Вторая", "done": True},
        ]

        self.assertTrue(delete_task(tasks, 1))
        self.assertEqual(
            tasks,
            [
                {"id": 5, "title": "Вторая", "done": True},
            ],
        )


if __name__ == "__main__":
    unittest.main()
