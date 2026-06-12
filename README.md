# Backend Journey

Учебный backend-проект: простой трекер задач с CLI-версией и REST API на FastAPI.

## Возможности

- создавать задачи;
- получать список задач;
- редактировать название и статус задачи;
- отмечать задачу выполненной;
- удалять задачи;
- сохранять данные в JSON-файл.

## Стек технологий

- Python;
- FastAPI;
- Uvicorn;
- Pydantic;
- unittest.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск FastAPI-версии

```bash
uvicorn app.main:app --reload
```

После запуска открой:

```text
http://127.0.0.1:8000
```

## Запуск CLI-версии

```bash
python cli.py
```

## Запуск тестов

```bash
python -m unittest discover -s tests -v
```

## API endpoints

- `GET /api/tasks` — получить список задач;
- `POST /api/tasks` — создать задачу;
- `PATCH /api/tasks/{task_id}` — обновить задачу;
- `PATCH /api/tasks/{task_id}/done` — отметить задачу выполненной;
- `DELETE /api/tasks/{task_id}` — удалить задачу.

## Что изучено

- структура FastAPI-приложения;
- разделение routers, services, storage, templates и static;
- REST API и HTTP-статусы;
- Pydantic-схемы и валидация входных данных;
- стабильные идентификаторы задач;
- базовые unit/API-тесты на `unittest`.
