import unittest

from tasks import (
    add_task,
    delete_task,
    get_tasks_text,
    mark_task_done,
    normalize_tasks,
    update_task,
)


class NormalizeTasksTest(unittest.TestCase):
    def test_normalize_tasks_keeps_valid_tasks_and_reassigns_ids(self):
        tasks = [
            {"id": 10, "title": "  First task  ", "done": False},
            {"title": "", "done": False},
            "broken",
            {"id": 99, "title": "Second task", "done": True},
        ]

        self.assertEqual(
            normalize_tasks(tasks),
            [
                {"id": 1, "title": "First task", "done": False},
                {"id": 2, "title": "Second task", "done": True},
            ],
        )


class AddTaskTest(unittest.TestCase):
    def test_add_task_appends_new_task(self):
        tasks = []

        result = add_task(tasks, " Learn tests ")

        self.assertTrue(result)
        self.assertEqual(
            tasks,
            [{"id": 1, "title": "Learn tests", "done": False}],
        )

    def test_add_task_rejects_empty_title(self):
        tasks = []

        result = add_task(tasks, "   ")

        self.assertFalse(result)
        self.assertEqual(tasks, [])


class GetTasksTextTest(unittest.TestCase):
    def test_get_tasks_text_returns_readable_lines_and_normalizes_tasks(self):
        tasks = [
            {"id": 7, "title": "Write code", "done": False},
            {"id": 8, "title": "Run tests", "done": True},
        ]

        self.assertEqual(
            get_tasks_text(tasks),
            [
                "1. Write code [Не выполнена]",
                "2. Run tests [Выполнена]",
            ],
        )
        self.assertEqual(
            tasks,
            [
                {"id": 1, "title": "Write code", "done": False},
                {"id": 2, "title": "Run tests", "done": True},
            ],
        )


class MarkTaskDoneTest(unittest.TestCase):
    def test_mark_task_done_updates_existing_task(self):
        tasks = [{"id": 1, "title": "Write tests", "done": False}]

        result = mark_task_done(tasks, 1)

        self.assertTrue(result)
        self.assertTrue(tasks[0]["done"])

    def test_mark_task_done_returns_false_for_missing_task(self):
        tasks = [{"id": 1, "title": "Write tests", "done": False}]

        result = mark_task_done(tasks, 2)

        self.assertFalse(result)
        self.assertFalse(tasks[0]["done"])


class UpdateTaskTest(unittest.TestCase):
    def test_update_task_changes_existing_task_title(self):
        tasks = [{"id": 1, "title": "Old title", "done": False}]

        result = update_task(tasks, 1, " New title ")

        self.assertTrue(result)
        self.assertEqual(tasks[0]["title"], "New title")

    def test_update_task_rejects_empty_title(self):
        tasks = [{"id": 1, "title": "Old title", "done": False}]

        result = update_task(tasks, 1, "   ")

        self.assertFalse(result)
        self.assertEqual(tasks[0]["title"], "Old title")

    def test_update_task_returns_false_for_missing_task(self):
        tasks = [{"id": 1, "title": "Old title", "done": False}]

        result = update_task(tasks, 2, "New title")

        self.assertFalse(result)
        self.assertEqual(tasks[0]["title"], "Old title")


class DeleteTaskTest(unittest.TestCase):
    def test_delete_task_removes_existing_task_and_normalizes_ids(self):
        tasks = [
            {"id": 1, "title": "First", "done": False},
            {"id": 2, "title": "Second", "done": False},
        ]

        result = delete_task(tasks, 1)

        self.assertTrue(result)
        self.assertEqual(
            tasks,
            [{"id": 1, "title": "Second", "done": False}],
        )

    def test_delete_task_returns_false_for_missing_task(self):
        tasks = [{"id": 1, "title": "Only task", "done": False}]

        result = delete_task(tasks, 2)

        self.assertFalse(result)
        self.assertEqual(tasks, [{"id": 1, "title": "Only task", "done": False}])


if __name__ == "__main__":
    unittest.main()
