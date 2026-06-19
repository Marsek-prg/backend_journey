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
* Фильтрация задач: все, активные и выполненные
* Поиск по части названия без учета регистра
* Статистика общего числа, активных и выполненных задач
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
│   ├── schemas/
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

Собрать Docker-образ:

```bash
docker build -t backend-journey-api .
```

Запустить контейнер:

```bash
docker run --rm -p 8000:8000 backend-journey-api
```

Или собрать и запустить приложение через Docker Compose:

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

## Desktop-версия

Desktop-версия использует готовый web-интерфейс и открывает его в отдельном окне приложения.
Web- и desktop-интерфейсы поддерживают фильтрацию, поиск и статистику задач.

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

Интерактивное меню позволяет показать все, активные или выполненные задачи и найти
задачи по тексту в названии.

## Тесты

```bash
python -m unittest discover -s tests -v
```

## Качество кода

Для проверки и форматирования кода используются Black и Ruff.

```bash
pip install -r requirements-dev.txt
black .
ruff check .
```

Для проверки без изменения файлов:

```bash
black --check .
ruff check .
```

## Автоматические проверки

GitHub Actions автоматически запускает тесты при каждом `push` и `pull_request`.
CI также проверяет, что Docker-образ проекта успешно собирается.

## Основные API endpoints

| Метод    | Endpoint                    | Описание                    |
| -------- | --------------------------- | --------------------------- |
| `GET`    | `/`                         | Web-интерфейс               |
| `GET`    | `/health`                   | Проверка состояния приложения |
| `GET`    | `/api/tasks`                | Получить список задач; параметры `status` и `q` |
| `GET`    | `/api/tasks/stats`          | Получить статистику задач   |
| `POST`   | `/api/tasks`                | Создать задачу              |
| `PATCH`  | `/api/tasks/{task_id}`      | Обновить задачу             |
| `PATCH`  | `/api/tasks/{task_id}/done` | Отметить задачу выполненной |
| `DELETE` | `/api/tasks/{task_id}`      | Удалить задачу              |

Параметр `status` принимает значения `all`, `active` и `completed`. Если параметр
не указан, API возвращает все задачи. Параметр `q` выполняет регистронезависимый
поиск по части `title`; его можно комбинировать со `status`.

Примеры:

```text
GET /api/tasks?status=active
GET /api/tasks?status=completed&q=отчет
GET /api/tasks/stats
```

## Версия

Текущая версия проекта: `v0.1.0`.

История изменений ведётся в `CHANGELOG.md`.

## Roadmap

Планируемые улучшения:

* Более надёжное JSON-хранилище
* Приоритеты задач
* Даты создания и обновления задач
* Улучшение UX web-интерфейса
