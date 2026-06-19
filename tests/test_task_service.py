import unittest

from app.services.task_service import (
    add_task,
    delete_task,
    filter_tasks_by_status,
    get_tasks_stats,
    get_tasks_text,
    mark_task_done,
    search_tasks,
)


class TaskServiceTest(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "title": "Купить хлеб", "done": False},
            {"id": 2, "title": "Написать TEST", "done": True},
            {"id": 3, "title": "Домашняя работа", "done": False},
        ]

    def test_filter_tasks_by_status(self):
        self.assertEqual(
            filter_tasks_by_status(self.tasks, "active"),
            [self.tasks[0], self.tasks[2]],
        )
        self.assertEqual(
            filter_tasks_by_status(self.tasks, "completed"),
            [self.tasks[1]],
        )

    def test_search_tasks_by_title_part_case_insensitive(self):
        self.assertEqual(search_tasks(self.tasks, "test"), [self.tasks[1]])
        self.assertEqual(search_tasks(self.tasks, "ХЛЕБ"), [self.tasks[0]])

    def test_get_tasks_stats(self):
        self.assertEqual(
            get_tasks_stats(self.tasks),
            {"total": 3, "active": 2, "completed": 1},
        )

    def test_add_task_rejects_empty_title(self):
        tasks = []

        result = add_task(tasks, "   ")

        self.assertIsNone(result)
        self.assertEqual(tasks, [])

    def test_add_mark_and_delete_task(self):
        tasks = []

        created_task = add_task(tasks, "Купить хлеб")

        self.assertEqual(
            created_task,
            {"id": 1, "title": "Купить хлеб", "done": False},
        )

        updated_task = mark_task_done(tasks, 1)
        self.assertEqual(
            updated_task,
            {"id": 1, "title": "Купить хлеб", "done": True},
        )

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
