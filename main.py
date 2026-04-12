import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("tasks.json is corrupted. Starting with empty task list.")
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def show_menu():
    print("\n--- Task Tracker ---")
    print("1. Add task")
    print("2. Show tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Exit")


def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")


def show_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    for task in tasks:
        status = "Done" if task["done"] else "Not done"
        print(f'{task["id"]}. {task["title"]} [{status}]')


def mark_task_done(tasks):
    if not tasks:
        print("No tasks available.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Enter task id to mark as done: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print("Task marked as done.")
            return

    print("Task not found.")


def delete_task(tasks):
    if not tasks:
        print("No tasks available.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Enter task id to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted.")
            return

    print("Task not found.")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()