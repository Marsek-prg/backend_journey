import os
import unittest
from pathlib import Path
from unittest.mock import patch

from app.core.paths import get_user_data_dir


class PathsTest(unittest.TestCase):
    def test_task_tracker_data_dir_overrides_default_data_directory(self):
        configured_dir = Path("custom") / "task-tracker-data"

        with patch.dict(
            os.environ,
            {"TASK_TRACKER_DATA_DIR": str(configured_dir)},
        ):
            self.assertEqual(get_user_data_dir(), configured_dir)


if __name__ == "__main__":
    unittest.main()
