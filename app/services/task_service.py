def get_next_task_id(tasks):
    ids = [task["id"] for task in tasks if isinstance(task.get("id"), int)]
    if not ids:
        return 1

    return max(ids) + 1


def normalize_tasks(tasks):
    normalized_tasks = []
    used_ids = set()
    next_id = 1

    for task in tasks:
        if not isinstance(task, dict):
            continue

        title = str(task.get("title", "")).strip()
        if not title:
            continue

        task_id = task.get("id")
        if not isinstance(task_id, int) or task_id in used_ids or task_id < 1:
            while next_id in used_ids:
                next_id += 1
            task_id = next_id

        used_ids.add(task_id)
        normalized_tasks.append(
            {
                "id": task_id,
                "title": title,
                "done": bool(task.get("done", False)),
            }
        )

    return normalized_tasks


def add_task(tasks, title):
    title = title.strip()
    if not title:
        return None

    task = {
        "id": get_next_task_id(tasks),
        "title": title,
        "done": False,
    }
    tasks.append(task)
    return task


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
            return task

    return None


def update_task(tasks, task_id, title=None, done=None):
    for task in tasks:
        if task["id"] != task_id:
            continue

        if title is not None:
            title = title.strip()
            if not title:
                return None
            task["title"] = title

        if done is not None:
            task["done"] = bool(done)

        return task

    return None


def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True

    return False
