from storage import load_tasks, save_tasks
from tasks import (
    add_task,
    delete_task,
    get_tasks_text,
    mark_task_done,
)


def show_menu():
    print("\n--- Трекер задач ---")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Отметить задачу выполненной")
    print("4. Удалить задачу")
    print("5. Выйти")


def add_task_from_input(tasks):
    title = input("Введите название задачи: ").strip()
    if not add_task(tasks, title):
        print("Название задачи не может быть пустым.")
        return

    save_tasks(tasks)
    print("Задача добавлена.")


def show_tasks(tasks):
    if not tasks:
        print("Задач пока нет.")
        return

    for line in get_tasks_text(tasks):
        print(line)


def mark_task_done_from_input(tasks):
    if not tasks:
        print("Нет доступных задач.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Введите id задачи для отметки: "))
    except ValueError:
        print("Введите корректное число.")
        return

    if mark_task_done(tasks, task_id):
        save_tasks(tasks)
        print("Задача отмечена выполненной.")
        return

    print("Задача не найдена.")


def delete_task_from_input(tasks):
    if not tasks:
        print("Нет доступных задач.")
        return

    show_tasks(tasks)

    try:
        task_id = int(input("Введите id задачи для удаления: "))
    except ValueError:
        print("Введите корректное число.")
        return

    if delete_task(tasks, task_id):
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
            add_task_from_input(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            mark_task_done_from_input(tasks)
        elif choice == "4":
            delete_task_from_input(tasks)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
