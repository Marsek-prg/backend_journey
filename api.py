from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from storage import load_tasks, save_tasks
from tasks import add_task, delete_task, mark_task_done, update_task


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    title: str = ""


class TaskUpdate(BaseModel):
    title: str = ""


@router.get("")
def get_tasks():
    return load_tasks()


@router.post("", status_code=201)
def create_task(task_data: TaskCreate):
    tasks = load_tasks()

    if not add_task(tasks, task_data.title):
        raise HTTPException(status_code=400, detail="Task title is required")

    save_tasks(tasks)
    return tasks


@router.patch("/{task_id}")
def edit_task(task_id: int, task_data: TaskUpdate):
    tasks = load_tasks()

    if not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")

    if not update_task(tasks, task_id, task_data.title):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(tasks)
    return tasks


@router.post("/{task_id}/done")
def complete_task(task_id: int):
    tasks = load_tasks()

    if not mark_task_done(tasks, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(tasks)
    return tasks


@router.delete("/{task_id}")
def remove_task(task_id: int):
    tasks = load_tasks()

    if not delete_task(tasks, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(tasks)
    return tasks
