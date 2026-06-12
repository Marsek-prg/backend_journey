const tasksList = document.querySelector("#tasks");
const taskForm = document.querySelector("#task-form");
const taskTitle = document.querySelector("#task-title");

async function loadTasks() {
  const response = await fetch("/api/tasks");
  const tasks = await response.json();

  tasksList.innerHTML = "";

  for (const task of tasks) {
    const item = document.createElement("li");
    const title = document.createElement("span");
    const doneButton = document.createElement("button");
    const deleteButton = document.createElement("button");

    title.textContent = `${task.id}. ${task.title} [${task.done ? "Выполнена" : "Не выполнена"}]`;
    doneButton.textContent = "Готово";
    deleteButton.textContent = "Удалить";

    doneButton.addEventListener("click", async () => {
      await fetch(`/api/tasks/${task.id}/done`, { method: "PATCH" });
      await loadTasks();
    });

    deleteButton.addEventListener("click", async () => {
      await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
      await loadTasks();
    });

    item.append(title, doneButton, deleteButton);
    tasksList.append(item);
  }
}

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = taskTitle.value.trim();
  if (!title) {
    return;
  }

  await fetch("/api/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  taskTitle.value = "";
  await loadTasks();
});

loadTasks();
