# Audit Service API

REST API для управления внутренними аудитами качества (АС ВАК).

## Стек
- Python 3.11 + FastAPI
- In-Memory хранение
- Docker / docker-compose
- GitHub Actions CI

## Эндпоинты
| Метод | URL | Описание |
|---|---|---|
| GET | /api/v1/audits/ | Список аудитов |
| GET | /api/v1/audits/{id} | Аудит по id |
| POST | /api/v1/audits/ | Создать аудит |
| DELETE | /api/v1/audits/{id} | Удалить аудит |

## Запуск локально
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload