const tasksList = document.querySelector("#tasks");
const taskForm = document.querySelector("#task-form");
const taskTitle = document.querySelector("#task-title");
const taskError = document.querySelector("#task-error");
const taskCount = document.querySelector("#task-count");
const taskSearch = document.querySelector("#task-search");
const filterButtons = document.querySelectorAll(".filter-button");
const statsTotal = document.querySelector("#stats-total");
const statsActive = document.querySelector("#stats-active");
const statsCompleted = document.querySelector("#stats-completed");
let currentStatus = "all";
let searchTimer;

function showFormError(message) {
  taskError.textContent = message;
  taskTitle.classList.toggle("input--error", Boolean(message));
  taskTitle.setAttribute("aria-invalid", String(Boolean(message)));
}

function createButton(text, className) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = text;
  button.className = `button ${className}`;
  return button;
}

function showEmptyState() {
  const emptyState = document.createElement("li");
  emptyState.className = "empty-state";
  const hasFilters = currentStatus !== "all" || taskSearch.value.trim();
  emptyState.innerHTML = hasFilters
    ? "<strong>Ничего не найдено</strong>Измените фильтр или поисковый запрос."
    : "<strong>Задач пока нет</strong>Добавьте первую задачу — она появится здесь.";
  tasksList.append(emptyState);
}

async function loadStats() {
  const response = await fetch("/api/tasks/stats");
  if (!response.ok) {
    throw new Error("Не удалось загрузить статистику.");
  }
  const stats = await response.json();
  statsTotal.textContent = stats.total;
  statsActive.textContent = stats.active;
  statsCompleted.textContent = stats.completed;
}

async function updateTask(taskId, data) {
  const response = await fetch(`/api/tasks/${taskId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Не удалось обновить задачу.");
  }
}

function startEditing(task, content, titleElement, editButton) {
  const input = document.createElement("input");
  input.className = "task-edit-input";
  input.value = task.title;
  input.setAttribute("aria-label", "Новое название задачи");
  content.replaceChild(input, titleElement);
  editButton.textContent = "Сохранить";
  input.focus();
  input.select();

  const save = async () => {
    const newTitle = input.value.trim();
    if (!newTitle) {
      input.focus();
      return;
    }

    await updateTask(task.id, { title: newTitle });
    await loadTasks();
  };

  editButton.onclick = save;
  input.addEventListener("keydown", async (event) => {
    if (event.key === "Enter") {
      await save();
    }
    if (event.key === "Escape") {
      await loadTasks();
    }
  });
}

function renderTask(task) {
  const item = document.createElement("li");
  const statusButton = document.createElement("button");
  const content = document.createElement("div");
  const title = document.createElement("span");
  const meta = document.createElement("span");
  const actions = document.createElement("div");
  const editButton = createButton("Изменить", "button--secondary");
  const deleteButton = createButton("Удалить", "button--danger");

  item.className = `task-item${task.done ? " task-item--completed" : ""}`;
  statusButton.type = "button";
  statusButton.className = "task-item__status";
  statusButton.textContent = "✓";
  statusButton.setAttribute(
    "aria-label",
    task.done ? `Задача «${task.title}» выполнена` : `Отметить задачу «${task.title}» выполненной`,
  );
  title.className = "task-item__title";
  title.textContent = task.title;
  meta.className = "task-item__meta";
  meta.textContent = task.done ? "Выполнено" : `Задача №${task.id}`;
  content.className = "task-item__content";
  actions.className = "task-item__actions";

  statusButton.addEventListener("click", async () => {
    if (task.done) {
      await updateTask(task.id, { done: false });
    } else {
      await fetch(`/api/tasks/${task.id}/done`, { method: "PATCH" });
    }
    await loadTasks();
  });

  editButton.addEventListener("click", () => {
    startEditing(task, content, title, editButton);
  });

  deleteButton.addEventListener("click", async () => {
    await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
    await loadTasks();
  });

  content.append(title, meta);
  actions.append(editButton, deleteButton);
  item.append(statusButton, content, actions);
  tasksList.append(item);
}

async function loadTasks() {
  const params = new URLSearchParams({ status: currentStatus });
  const query = taskSearch.value.trim();
  if (query) {
    params.set("q", query);
  }
  const response = await fetch(`/api/tasks?${params}`);
  if (!response.ok) {
    throw new Error("Не удалось загрузить задачи.");
  }
  const tasks = await response.json();

  await loadStats();

  tasksList.innerHTML = "";
  taskCount.textContent = tasks.length ? `${tasks.length} шт.` : "";

  if (tasks.length === 0) {
    showEmptyState();
    return;
  }

  tasks.forEach(renderTask);
}

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = taskTitle.value.trim();
  if (!title) {
    showFormError("Введите название задачи.");
    taskTitle.focus();
    return;
  }

  showFormError("");
  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    showFormError("Не удалось добавить задачу. Попробуйте ещё раз.");
    return;
  }

  taskTitle.value = "";
  await loadTasks();
});

taskTitle.addEventListener("input", () => {
  if (taskTitle.value.trim()) {
    showFormError("");
  }
});

filterButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    currentStatus = button.dataset.status;
    filterButtons.forEach((item) => {
      item.classList.toggle("filter-button--active", item === button);
    });
    await loadTasks();
  });
});

taskSearch.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadTasks, 250);
});

loadTasks();
