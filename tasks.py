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


def add_task(tasks, title):
    title = title.strip()
    if not title:
        return False

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
    }
    tasks.append(task)
    return True


def get_tasks_text(tasks):
    tasks[:] = normalize_tasks(tasks)

    lines = []
    for task in tasks:
        status = "Выполнена" if task["done"] else "Не выполнена"
        lines.append(f'{task["id"]}. {task["title"]} [{status}]')

    return lines


def mark_task_done(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True

    return False


def update_task(tasks, task_id, title):
    title = title.strip()
    if not title:
        return False

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = title
            return True

    return False


def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            tasks[:] = normalize_tasks(tasks)
            return True

    return False
