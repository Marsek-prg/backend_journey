# Backend Journey

Мой путь в backend-разработку с нуля.

## Первый проект

CLI Task Tracker на Python.

## Что уже реализовано

- добавить задачу
- показать задачи
- изменить название задачи
- отметить задачу выполненной
- удалить задачу
- сохранить задачи в JSON
- открыть трекер задач в браузере
- REST API на FastAPI
- автоматическая документация API
- unit-тесты для логики задач и API

## Структура проекта

```text
api.py              REST API для задач
web.py              запуск FastAPI и HTML-страница
main.py             CLI-версия приложения
tasks.py            логика работы с задачами
storage.py          загрузка и сохранение задач в JSON
tests/test_tasks.py тесты логики задач
tests/test_web.py   тесты API
requirements.txt    зависимости проекта
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск CLI

```bash
python main.py
```

## Запуск в браузере

```bash
python web.py
```

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:8000
```

## API-документация

FastAPI автоматически создает документацию:

```text
http://127.0.0.1:8000/docs
```

## REST API

### Получить список задач

```http
GET /api/tasks
```

Пример ответа:

```json
[
  {
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
  }
]
```

### Добавить задачу

```http
POST /api/tasks
Content-Type: application/json
```

Пример тела запроса:

```json
{
  "title": "Learn FastAPI"
}
```

### Изменить задачу

```http
PATCH /api/tasks/{id}
Content-Type: application/json
```

Пример тела запроса:

```json
{
  "title": "Learn REST API"
}
```

### Отметить задачу выполненной

```http
POST /api/tasks/{id}/done
```

### Удалить задачу

```http
DELETE /api/tasks/{id}
```

## Тесты

```bash
python -m unittest discover -s tests -v
```
