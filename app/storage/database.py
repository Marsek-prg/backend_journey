import json

from app.core.paths import get_user_data_dir
from app.services.task_service import normalize_tasks


TASKS_FILE = get_user_data_dir() / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("tasks.json поврежден. Начинаем с пустого списка задач.")
        return []

    if not isinstance(data, list):
        print("tasks.json содержит неверный формат. Начинаем с пустого списка задач.")
        return []

    tasks = normalize_tasks(data)
    if tasks != data:
        save_tasks(tasks)

    return tasks


def save_tasks(tasks):
    tasks = normalize_tasks(tasks)
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
