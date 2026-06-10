import webbrowser

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel

from storage import load_tasks, save_tasks
from tasks import add_task, delete_task, mark_task_done


HOST = "127.0.0.1"
PORT = 8000

app = FastAPI(title="Task Tracker")


class TaskCreate(BaseModel):
    title: str = ""


PAGE = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Трекер задач</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f4f7f5;
      --surface: #ffffff;
      --text: #17201b;
      --muted: #66736b;
      --line: #dce4df;
      --primary: #256d4f;
      --primary-hover: #1f5d44;
      --danger: #b13d3d;
      --danger-hover: #913232;
      --done: #eef6f1;
      --shadow: 0 12px 34px rgba(23, 32, 27, 0.09);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .app {
      width: min(920px, calc(100% - 32px));
      margin: 0 auto;
      padding: 40px 0;
    }

    header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 22px;
    }

    h1 {
      margin: 0;
      font-size: 34px;
      line-height: 1.1;
      font-weight: 700;
      letter-spacing: 0;
    }

    .stats {
      color: var(--muted);
      font-size: 15px;
      white-space: nowrap;
    }

    .panel {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      padding: 16px;
      border-bottom: 1px solid var(--line);
    }

    input {
      width: 100%;
      min-height: 44px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 12px;
      font-size: 16px;
      color: var(--text);
      background: #fff;
    }

    input:focus {
      border-color: var(--primary);
      outline: 3px solid rgba(37, 109, 79, 0.15);
    }

    button {
      min-height: 40px;
      border: 0;
      border-radius: 6px;
      padding: 0 14px;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      color: #fff;
      background: var(--primary);
    }

    button:hover {
      background: var(--primary-hover);
    }

    button.secondary {
      color: var(--primary);
      border: 1px solid var(--line);
      background: #fff;
    }

    button.secondary:hover {
      background: #eef6f1;
    }

    button.danger {
      background: var(--danger);
    }

    button.danger:hover {
      background: var(--danger-hover);
    }

    .tasks {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .task {
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
    }

    .task:last-child {
      border-bottom: 0;
    }

    .task.done {
      background: var(--done);
    }

    .task-title {
      min-width: 0;
      overflow-wrap: anywhere;
      font-size: 16px;
      line-height: 1.35;
    }

    .task.done .task-title {
      color: var(--muted);
      text-decoration: line-through;
    }

    .task-id {
      width: 30px;
      height: 30px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line);
      border-radius: 50%;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      background: #fff;
    }

    .actions {
      display: flex;
      gap: 8px;
    }

    .empty {
      padding: 34px 16px;
      text-align: center;
      color: var(--muted);
    }

    @media (max-width: 640px) {
      .app {
        width: min(100% - 20px, 920px);
        padding: 20px 0;
      }

      header {
        align-items: flex-start;
        flex-direction: column;
      }

      h1 {
        font-size: 28px;
      }

      form {
        grid-template-columns: 1fr;
      }

      .task {
        grid-template-columns: auto 1fr;
      }

      .actions {
        grid-column: 2;
        flex-wrap: wrap;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <header>
      <h1>Трекер задач</h1>
      <div class="stats" id="stats"></div>
    </header>

    <section class="panel">
      <form id="task-form">
        <input id="title" name="title" placeholder="Новая задача" autocomplete="off" required>
        <button type="submit">Добавить</button>
      </form>
      <ul class="tasks" id="tasks"></ul>
    </section>
  </main>

  <script>
    const form = document.querySelector("#task-form");
    const titleInput = document.querySelector("#title");
    const list = document.querySelector("#tasks");
    const stats = document.querySelector("#stats");

    async function request(path, options = {}) {
      const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options,
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      return response.json();
    }

    function render(tasks) {
      const doneCount = tasks.filter((task) => task.done).length;
      stats.textContent = `${tasks.length} всего, ${doneCount} выполнено`;

      if (tasks.length === 0) {
        list.innerHTML = `<li class="empty">Задач пока нет</li>`;
        return;
      }

      list.innerHTML = "";
      for (const task of tasks) {
        const item = document.createElement("li");
        item.className = `task${task.done ? " done" : ""}`;
        item.innerHTML = `
          <span class="task-id">${task.id}</span>
          <span class="task-title"></span>
          <span class="actions">
            <button class="secondary" type="button" data-action="done" data-id="${task.id}">
              Выполнено
            </button>
            <button class="danger" type="button" data-action="delete" data-id="${task.id}">
              Удалить
            </button>
          </span>
        `;
        item.querySelector(".task-title").textContent = task.title;
        list.append(item);
      }
    }

    async function loadTasks() {
      render(await request("/api/tasks"));
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const title = titleInput.value.trim();
      if (!title) {
        return;
      }

      await request("/api/tasks", {
        method: "POST",
        body: JSON.stringify({ title }),
      });
      titleInput.value = "";
      await loadTasks();
      titleInput.focus();
    });

    list.addEventListener("click", async (event) => {
      const button = event.target.closest("button");
      if (!button) {
        return;
      }

      const id = button.dataset.id;
      if (button.dataset.action === "done") {
        await request(`/api/tasks/${id}/done`, { method: "POST" });
      }

      if (button.dataset.action === "delete") {
        await request(`/api/tasks/${id}`, { method: "DELETE" });
      }

      await loadTasks();
    });

    loadTasks();
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def show_page():
    return PAGE


@app.get("/favicon.ico", status_code=204)
def favicon():
    return Response(status_code=204)


@app.get("/api/tasks")
def get_tasks():
    return load_tasks()


@app.post("/api/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    tasks = load_tasks()

    if not add_task(tasks, task_data.title):
        raise HTTPException(status_code=400, detail="Task title is required")

    save_tasks(tasks)
    return tasks


@app.post("/api/tasks/{task_id}/done")
def complete_task(task_id: int):
    tasks = load_tasks()

    if not mark_task_done(tasks, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(tasks)
    return tasks


@app.delete("/api/tasks/{task_id}")
def remove_task(task_id: int):
    tasks = load_tasks()

    if not delete_task(tasks, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(tasks)
    return tasks


def main():
    url = f"http://{HOST}:{PORT}"
    print(f"Трекер задач запущен: {url}")
    webbrowser.open(url)
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
