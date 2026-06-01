import json
from pathlib import Path

TASKS_FILE = Path(__file__).resolve().parent / "tasks.json"


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

    return normalize_tasks(data)


def normalize_tasks(tasks):
    normalized_tasks = []

    for task in tasks:
        if not isinstance(task, dict):
            continue

        title = str(task.get("title", "")).strip()
        if not title:
            continue

        normalized_tasks.append({
            "id": len(normalized_tasks) + 1,
            "title": title,
            "done": bool(task.get("done", False)),
        })

    return normalized_tasks


def save_tasks(tasks):
    tasks = normalize_tasks(tasks)

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def show_menu():
    print("\n--- Трекер задач ---")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("5. Выйти")


def add_task(tasks):
    title = input("Введите название задачи: ").strip()
    if not title:
        print("Название задачи не может быть пустым.")
        return

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена.")


def show_tasks(tasks):
    if not tasks:
        print("Задач пока нет.")
        return

    tasks[:] = normalize_tasks(tasks)

    for task in tasks:
        status = "Выполнена" if task["done"] else "Не выполнена"
        print(f'{task["id"]}. {task["title"]} [{status}]')


def mark_task_done(tasks):
    if not tasks:
        print("Нет доступных задач.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Введите id задачи для отметки: "))
    except ValueError:
        print("Введите корректное число.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print("Задача отмечена выполненной.")
            return

    print("Задача не найдена.")


def delete_task(tasks):
    if not tasks:
        print("Нет доступных задач.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Введите id задачи для удаления: "))
    except ValueError:
        print("Введите корректное число.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            tasks[:] = normalize_tasks(tasks)
            save_tasks(tasks)
            print("Задача удалена.")
            return

    print("Задача не найдена.")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
