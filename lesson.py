import json
from pathlib import Path


TASKS_FILE = Path(__file__).resolve().parent / 'lesson_tasks.json'


def show_tasks(tasks):
    for task in tasks:
        if task['done']:
            status = 'Выполнена'
        else:
            status = 'Не выполнена'

        print('Задача:', task['title'], 'Статус:', status)


def add_task(tasks, title):
    tasks.append({'title': title, 'done': False})


def mark_done(tasks, title):
    for task in tasks:
        if task['title'] == title:
            task['done'] = True


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False)


def load_tasks():
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def main():
    # загрузка
    tasks = load_tasks()

    # работа программы
    add_task(tasks, 'Купить хлеб')
    add_task(tasks, 'Купить сервер VPN')

    # сохранение
    save_tasks(tasks)

    show_tasks(tasks)


if __name__ == '__main__':
    main()
