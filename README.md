# Проект: Автотесты API и БД онлайн-кинотеатра

## Описание
Данный проект содержит автоматизированные тесты для backend-сервиса онлайн-кинотеатра.

Покрываются:
- API методы работы с фильмами
- авторизация пользователей
- проверка данных в базе данных
- негативные сценарии
- роли и доступы (RBAC)

---

## Используемый стек
- Python 3.10+
- Pytest
- Requests
- SQLAlchemy
- Pydantic
- Allure
- PostgreSQL

---

## Структура проекта
- tests/ — API и DB тесты
- clients/ — API клиенты (movies, auth, users)
- db_models/ — модели базы данных
- db_requester/ — работа с БД
- data_generator/ — генерация тестовых данных
- models/ — Pydantic модели
- conftest.py — фикстуры pytest

---

## Запуск тестов

Установка зависимостей:
```bash
pip install -r requirements.txt
```

Запуск всех тестов:
```bash
pytest
```

Запуск тестов по маркам:
```bash
pytest -m movies
pytest -m db
pytest -m negative
```

Запуск конкретного файла:
```bash
pytest tests/movies/test_get_movies.py
```

Запуск с Аллюр отчетом:
```bash
pytest --alluredir=allure-results
```

Просмотр Аллюр отчета:
```bash
C:\Users\димон\scoop\apps\allure\current\bin\allure.bat serve allure-results
```
