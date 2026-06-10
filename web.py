import webbrowser

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from api import router as tasks_router


HOST = "127.0.0.1"
PORT = 8000

app = FastAPI(title="Task Tracker")
app.include_router(tasks_router)


PAGE = """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Трекер задач</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #eef3f0;
      --bg-soft: #dfe9e3;
      --surface: #ffffff;
      --surface-strong: #f8fbf9;
      --text: #17201b;
      --muted: #6d7a72;
      --line: #d7e1db;
      --primary: #256d59;
      --primary-hover: #1e5848;
      --primary-soft: #e3f1eb;
      --accent: #c78f3e;
      --accent-soft: #fff3df;
      --danger: #b44949;
      --danger-hover: #943a3a;
      --done: #edf6f1;
      --shadow: 0 18px 44px rgba(28, 42, 34, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Arial, sans-serif;
      background:
        linear-gradient(180deg, rgba(37, 109, 89, 0.11), transparent 280px),
        radial-gradient(circle at top left, rgba(199, 143, 62, 0.16), transparent 320px),
        var(--bg);
      color: var(--text);
    }

    .app {
      width: min(980px, calc(100% - 32px));
      margin: 0 auto;
      padding: 44px 0;
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 24px;
    }

    h1 {
      margin: 0;
      font-size: 38px;
      line-height: 1.1;
      font-weight: 700;
      letter-spacing: 0;
    }

    .subtitle {
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.45;
    }

    .stats {
      display: inline-flex;
      align-items: center;
      min-height: 38px;
      padding: 0 14px;
      border: 1px solid rgba(37, 109, 89, 0.18);
      border-radius: 999px;
      color: var(--primary);
      background: rgba(255, 255, 255, 0.72);
      font-size: 15px;
      font-weight: 700;
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
      gap: 12px;
      padding: 18px;
      border-bottom: 1px solid var(--line);
      background: var(--surface-strong);
    }

    input {
      width: 100%;
      min-height: 48px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 14px;
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

    button[hidden] {
      display: none;
    }

    button:focus-visible {
      outline: 3px solid rgba(37, 109, 89, 0.2);
      outline-offset: 2px;
    }

    button:hover {
      background: var(--primary-hover);
    }

    .add-button {
      min-height: 48px;
      padding: 0 20px;
      font-size: 15px;
    }

    button.secondary {
      color: var(--primary);
      border: 1px solid var(--line);
      background: #fff;
    }

    button.secondary:hover {
      background: var(--primary-soft);
    }

    button.icon-button {
      width: 38px;
      min-height: 38px;
      padding: 0;
      display: grid;
      place-items: center;
      color: var(--text);
      border: 1px solid var(--line);
      background: #fff;
      font-size: 18px;
      line-height: 1;
    }

    button.icon-button:hover {
      border-color: rgba(37, 109, 89, 0.35);
      background: var(--primary-soft);
    }

    button.danger {
      background: var(--danger);
    }

    button.danger:hover {
      background: var(--danger-hover);
    }

    button.icon-button.danger {
      color: #fff;
      border-color: transparent;
      background: var(--danger);
    }

    button.icon-button.danger:hover {
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
      gap: 14px;
      padding: 15px 18px;
      border-bottom: 1px solid var(--line);
      transition: background 0.15s ease, transform 0.15s ease;
    }

    .task:hover {
      background: #fbfdfc;
    }

    .task:last-child {
      border-bottom: 0;
    }

    .task.done {
      background: var(--done);
    }

    .task-title {
      grid-column: 2;
      min-width: 0;
      overflow-wrap: anywhere;
      font-size: 16px;
      line-height: 1.45;
    }

    .task-edit {
      grid-column: 2;
      display: none;
      min-height: 40px;
      font-size: 15px;
    }

    .task.editing .task-title {
      display: none;
    }

    .task.editing .task-edit {
      display: block;
    }

    .task.editing {
      background: var(--accent-soft);
    }

    .task.done .task-title {
      color: var(--muted);
      text-decoration: line-through;
    }

    .task-id {
      width: 34px;
      height: 34px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(37, 109, 89, 0.18);
      border-radius: 50%;
      color: var(--primary);
      font-size: 13px;
      font-weight: 700;
      background: var(--primary-soft);
    }

    .actions {
      grid-column: 3;
      display: flex;
      gap: 8px;
    }

    .empty {
      padding: 42px 16px;
      text-align: center;
      color: var(--muted);
      background: linear-gradient(180deg, #fff, var(--surface-strong));
    }

    .empty strong {
      display: block;
      margin-bottom: 6px;
      color: var(--text);
      font-size: 18px;
    }

    .empty span {
      font-size: 14px;
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
        font-size: 30px;
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

      button.icon-button {
        width: 40px;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <header>
      <div>
        <h1>Трекер задач</h1>
        <p class="subtitle">План на день без лишнего шума</p>
      </div>
      <div class="stats" id="stats"></div>
    </header>

    <section class="panel">
      <form id="task-form">
        <input id="title" name="title" placeholder="Новая задача" autocomplete="off" required>
        <button class="add-button" type="submit">Добавить</button>
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
        list.innerHTML = `
          <li class="empty">
            <strong>Задач пока нет</strong>
            <span>Добавьте первую задачу и начните список.</span>
          </li>
        `;
        return;
      }

      list.innerHTML = "";
      for (const task of tasks) {
        const item = document.createElement("li");
        item.className = `task${task.done ? " done" : ""}`;
        item.innerHTML = `
          <span class="task-id">${task.id}</span>
          <span class="task-title"></span>
          <input class="task-edit" type="text" aria-label="Название задачи">
          <span class="actions">
            <button class="icon-button" type="button" data-action="done" data-id="${task.id}" title="Отметить выполненной" aria-label="Отметить выполненной">
              ✓
            </button>
            <button class="icon-button" type="button" data-action="edit" data-id="${task.id}" title="Изменить задачу" aria-label="Изменить задачу">
              ✎
            </button>
            <button class="icon-button" type="button" data-action="save" data-id="${task.id}" title="Сохранить задачу" aria-label="Сохранить задачу" hidden>
              ✓
            </button>
            <button class="icon-button" type="button" data-action="cancel" data-id="${task.id}" title="Отменить изменение" aria-label="Отменить изменение" hidden>
              ×
            </button>
            <button class="icon-button danger" type="button" data-action="delete" data-id="${task.id}" title="Удалить задачу" aria-label="Удалить задачу">
              ×
            </button>
          </span>
        `;
        item.querySelector(".task-title").textContent = task.title;
        item.querySelector(".task-edit").value = task.title;
        list.append(item);
      }
    }

    function setEditMode(item, isEditing) {
      item.classList.toggle("editing", isEditing);
      item.querySelector('[data-action="done"]').hidden = isEditing;
      item.querySelector('[data-action="edit"]').hidden = isEditing;
      item.querySelector('[data-action="delete"]').hidden = isEditing;
      item.querySelector('[data-action="save"]').hidden = !isEditing;
      item.querySelector('[data-action="cancel"]').hidden = !isEditing;

      if (isEditing) {
        const input = item.querySelector(".task-edit");
        input.focus();
        input.select();
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
      const item = button.closest(".task");
      if (button.dataset.action === "done") {
        await request(`/api/tasks/${id}/done`, { method: "POST" });
      }

      if (button.dataset.action === "edit") {
        setEditMode(item, true);
        return;
      }

      if (button.dataset.action === "cancel") {
        setEditMode(item, false);
        return;
      }

      if (button.dataset.action === "save") {
        const title = item.querySelector(".task-edit").value.trim();
        if (!title) {
          return;
        }

        await request(`/api/tasks/${id}`, {
          method: "PATCH",
          body: JSON.stringify({ title }),
        });
      }

      if (button.dataset.action === "delete") {
        await request(`/api/tasks/${id}`, { method: "DELETE" });
      }

      await loadTasks();
    });

    list.addEventListener("keydown", async (event) => {
      const input = event.target.closest(".task-edit");
      if (!input) {
        return;
      }

      const item = input.closest(".task");
      if (event.key === "Escape") {
        setEditMode(item, false);
        return;
      }

      if (event.key === "Enter") {
        event.preventDefault();
        const title = input.value.trim();
        if (!title) {
          return;
        }

        const id = item.querySelector("[data-id]").dataset.id;
        await request(`/api/tasks/${id}`, {
          method: "PATCH",
          body: JSON.stringify({ title }),
        });
        await loadTasks();
      }
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


def main():
    url = f"http://{HOST}:{PORT}"
    print(f"Трекер задач запущен: {url}")
    webbrowser.open(url)
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
