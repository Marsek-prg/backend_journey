import json
import sqlite3
from pathlib import Path

from tasks import normalize_tasks


TASKS_DB = Path(__file__).resolve().parent / "tasks.db"
LEGACY_TASKS_FILE = Path(__file__).resolve().parent / "tasks.json"


def get_connection():
    connection = sqlite3.connect(TASKS_DB)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def migrate_legacy_json():
    if TASKS_DB.exists() or not LEGACY_TASKS_FILE.exists():
        return

    try:
        with open(LEGACY_TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return

    if isinstance(data, list):
        save_tasks(data)


def load_tasks():
    migrate_legacy_json()
    init_db()

    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
    finally:
        connection.close()

    return normalize_tasks([
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }
        for row in rows
    ])


def save_tasks(tasks):
    tasks = normalize_tasks(tasks)
    init_db()

    connection = get_connection()
    try:
        connection.execute("DELETE FROM tasks")
        connection.executemany(
            "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
            [
                (task["id"], task["title"], int(task["done"]))
                for task in tasks
            ],
        )
        connection.commit()
    finally:
        connection.close()
