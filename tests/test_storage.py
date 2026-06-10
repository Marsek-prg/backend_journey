import tempfile
import unittest
from pathlib import Path

import storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_tasks_db = storage.TASKS_DB
        self.original_legacy_tasks_file = storage.LEGACY_TASKS_FILE
        storage.TASKS_DB = Path(self.temp_dir.name) / "tasks.db"
        storage.LEGACY_TASKS_FILE = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        storage.TASKS_DB = self.original_tasks_db
        storage.LEGACY_TASKS_FILE = self.original_legacy_tasks_file
        self.temp_dir.cleanup()

    def test_load_tasks_returns_empty_list_when_database_is_new(self):
        self.assertEqual(storage.load_tasks(), [])

    def test_save_tasks_writes_tasks_to_sqlite_database(self):
        tasks = [
            {"id": 1, "title": "Write storage tests", "done": False},
            {"id": 2, "title": "Use SQLite", "done": True},
        ]

        storage.save_tasks(tasks)

        self.assertEqual(storage.load_tasks(), tasks)

    def test_save_tasks_normalizes_tasks_before_saving(self):
        tasks = [
            {"id": 10, "title": " First ", "done": False},
            {"id": 99, "title": "", "done": False},
            {"id": 20, "title": "Second", "done": True},
        ]

        storage.save_tasks(tasks)

        self.assertEqual(
            storage.load_tasks(),
            [
                {"id": 1, "title": "First", "done": False},
                {"id": 2, "title": "Second", "done": True},
            ],
        )

    def test_load_tasks_migrates_legacy_json_file_to_sqlite(self):
        storage.LEGACY_TASKS_FILE.write_text(
            '[{"id": 5, "title": " Legacy task ", "done": true}]',
            encoding="utf-8",
        )

        self.assertEqual(
            storage.load_tasks(),
            [{"id": 1, "title": "Legacy task", "done": True}],
        )
        self.assertTrue(storage.TASKS_DB.exists())


if __name__ == "__main__":
    unittest.main()
