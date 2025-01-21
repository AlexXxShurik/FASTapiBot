# BotFASTapi1

## Описание
Проект представляет собой FastAPI API, связанное с Telegram-ботом на Aiogram. Используется база данных PostgreSQL, SQLAlchemy и Pydantic для валидации данных. Проект упакован в Docker-контейнер для удобства деплоя и запуска.

## Структура проекта
- **app/**: Основной код приложения.
  - **api/**: Роуты и логика API.
  - **db/**: Модели базы данных и взаимодействие с PostgreSQL.
  - **services/**: Логика работы с сервисами и сторонними API.
  - **bot/**: Логика Telegram-бота с использованием Aiogram.
- **Dockerfile**: Dockerfile для создания контейнера.
- **docker-compose.yml**: Файл конфигурации для запуска приложения и базы данных в Docker.
- **requirements.txt**: Список зависимостей Python.
- **.env**: Конфигурационный файл с переменными окружения (не забудьте добавить его в `.gitignore`).
- **README.md**: Документация проекта.

## Требования
- Python >= 3.8
- PostgreSQL
- Docker (опционально)

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone <url вашего репозитория>
    cd BotFASTapi1
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` с необходимыми переменными окружения. Пример содержимого:

    ```env
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=fastDB
    BOT_API_TOKEN=your-telegram-bot-api-token
    DATABASE_URL=postgresql://user:password@localhost/fastDB
    ```

5. Для запуска базы данных и приложения с помощью Docker используйте команду:

    ```bash
    docker-compose up --build
    ```

    Это создаст контейнеры для базы данных и сервиса API.

## Запуск

1. Запуск приложения в виртуальном окружении:

    ```bash
    uvicorn app.main:app --reload
    ```

2. Запуск бота:

    Для запуска бота нужно запустить соответствующий скрипт. Например:

    ```bash
    python app/bot/main.py
    ```

## Примечания

- Для разработки можно использовать среду разработки PyCharm или VSCode.
- Параметры для подключения к базе данных могут быть настроены в `.env` файле.
