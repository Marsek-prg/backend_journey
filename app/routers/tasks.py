from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, constr

from app.services.task_service import (
    add_task,
    delete_task,
    mark_task_done,
    update_task,
)
from app.storage import database

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)


class TaskUpdate(BaseModel):
    title: constr(strip_whitespace=True, min_length=1) | None = None
    done: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool


@router.get("", response_model=list[TaskResponse])
def list_tasks():
    return database.load_tasks()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    tasks = database.load_tasks()
    created_task = add_task(tasks, task.title)

    database.save_tasks(tasks)
    return created_task


@router.patch("/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, task: TaskUpdate):
    tasks = database.load_tasks()
    updated_task = update_task(tasks, task_id, title=task.title, done=task.done)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    database.save_tasks(tasks)
    return updated_task


@router.patch("/{task_id}/done", response_model=TaskResponse)
def complete_task(task_id: int):
    tasks = database.load_tasks()
    updated_task = mark_task_done(tasks, task_id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    database.save_tasks(tasks)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int):
    tasks = database.load_tasks()
    if not delete_task(tasks, task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена.")

    database.save_tasks(tasks)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
