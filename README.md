# Task Tracker

Task Tracker —  Python/FastAPI проект для управления задачами с несколькими вариантами запуска: Web/API, CLI, Desktop-приложение для Windows и Docker.

Проект начинался как простой консольный список задач, но постепенно был расширен до полноценного проекта с REST API,
веб-интерфейсом, desktop-версией, Docker-запуском, тестами и сборкой `.exe`.

## Возможности

* Просмотр списка задач
* Добавление новой задачи
* Редактирование задачи
* Отметка задачи как выполненной
* Удаление задачи
* Хранение задач в локальном JSON-файле
* Web-интерфейс на FastAPI
* REST API для работы с задачами
* CLI-версия
* Desktop-версия для Windows
* Docker-запуск web/API-версии
* Unit/API-тесты

## Варианты запуска

| Вариант        | Команда / способ                | Для чего нужен                      |
| -------------- | ------------------------------- | ----------------------------------- |
| Web/API        | `uvicorn app.main:app --reload` | Локальная разработка и проверка API |
| CLI            | `python cli.py`                 | Консольная версия приложения        |
| Desktop        | `python desktop.py`             | Desktop-запуск через Python         |
| Windows `.exe` | GitHub Releases                 | Запуск без установленного Python    |
| Docker         | `docker compose up --build`     | Запуск web/API в контейнере         |

## Стек технологий

* Python
* FastAPI
* Uvicorn
* HTML
* CSS
* JavaScript
* pywebview
* PyInstaller
* Docker
* Docker Compose
* unittest
* httpx

## Структура проекта

```text
backend_journey/
├── app/
│   ├── core/
│   │   └── paths.py
│   ├── routers/
│   │   └── tasks.py
│   ├── services/
│   │   └── task_service.py
│   ├── storage/
│   │   └── database.py
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   └── main.py
├── scripts/
├── tests/
├── cli.py
├── desktop.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-desktop.txt
├── requirements-build.txt
└── README.md
```

## Быстрый запуск Web/API

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска приложение будет доступно:

```text
http://127.0.0.1:8000
```

API-документация:

```text
http://127.0.0.1:8000/docs
```

## Запуск через Docker

```bash
docker compose up --build
```

После запуска открой:

```text
http://127.0.0.1:8000
```

Остановить контейнер:

```bash
docker compose down
```

Остановить контейнер и удалить сохранённые задачи:

```bash
docker compose down -v
```

Данные в Docker сохраняются в volume `tasktracker_data`.

## Desktop-версия

Desktop-версия использует готовый web-интерфейс и открывает его в отдельном окне приложения.

Установка desktop-зависимостей:

```bash
pip install -r requirements-desktop.txt
```

Запуск:

```bash
python desktop.py
```

## Windows `.exe`

Готовую Windows-версию можно скачать в разделе Releases.

Как запустить:

1. Скачать архив `TaskTracker_win.zip`
2. Распаковать архив
3. Открыть папку `TaskTracker`
4. Запустить `TaskTracker.exe`

Python устанавливать не нужно.

Данные desktop-версии сохраняются в:

```text
%APPDATA%\TaskTracker\tasks.json
```

## CLI-версия

```bash
python cli.py
```

## Тесты

```bash
python -m unittest discover -s tests -v
```

## Основные API endpoints

| Метод    | Endpoint                    | Описание                    |
| -------- | --------------------------- | --------------------------- |
| `GET`    | `/`                         | Web-интерфейс               |
| `GET`    | `/api/tasks`                | Получить список задач       |
| `POST`   | `/api/tasks`                | Создать задачу              |
| `PATCH`  | `/api/tasks/{task_id}`      | Обновить задачу             |
| `POST`   | `/api/tasks/{task_id}/done` | Отметить задачу выполненной |
| `DELETE` | `/api/tasks/{task_id}`      | Удалить задачу              |


## Roadmap

Планируемые улучшения:

* GitHub Actions для автоматического запуска тестов
* Ruff и Black для проверки качества кода
* Отдельные Pydantic-схемы для API
* Health-check endpoint
* Улучшенный Docker healthcheck
* Changelog и версионирование
* Более надёжное JSON-хранилище
* Фильтры задач
* Приоритеты задач
* Даты создания и обновления задач
* Улучшение UX web-интерфейса