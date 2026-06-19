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

## Запуск через Docker

Собери образ и запусти web/API-версию приложения:

```bash
docker compose up --build
```

После запуска открой:

```text
http://127.0.0.1:8000
```

Задачи сохраняются в Docker volume `tasktracker_data`, поэтому остаются после
остановки и повторного запуска контейнера.

Остановить контейнеры:

```bash
docker compose down
```

Чтобы вместе с контейнерами удалить volume и все сохранённые задачи:

```bash
docker compose down -v
```

## Запуск CLI-версии

```bash
python cli.py
```

## Desktop-версия

Desktop-версия использует готовый web-интерфейс Task Tracker внутри обычного
окна Windows. При запуске FastAPI-сервер работает локально в фоновом потоке, а
`pywebview` открывает приложение без отдельного окна браузера.

Установи зависимости desktop-версии:

```bash
pip install -r requirements-desktop.txt
```

Запусти приложение:

```bash
python desktop.py
```

На Windows для отображения окна может потребоваться Microsoft Edge WebView2
Runtime. Обычно он уже установлен в Windows 10 и Windows 11. Если `pywebview`
сообщает об отсутствии web-компонента, установи WebView2 Runtime вручную с
официального сайта Microsoft.

Задачи сохраняются в пользовательской папке `%APPDATA%\TaskTracker\tasks.json`,
поэтому данные не зависят от расположения исходников или `.exe`.

## Сборка desktop-приложения в `.exe`

Основной способ сборки на Windows — скрипт `scripts\build_desktop.bat`.
Запускай команды из корня проекта:

```bash
pip install -r requirements-desktop.txt
pip install -r requirements-build.txt
scripts\build_desktop.bat
```

Скрипт использует Python из `.venv`, устанавливает необходимые зависимости и
создаёт сборку PyInstaller в режиме `onedir`. Готовое приложение находится по
пути `dist/TaskTracker/TaskTracker.exe`.

Каталоги `dist/`, `build/` и создаваемый PyInstaller файл `.spec` являются
артефактами сборки — их не нужно коммитить.

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
