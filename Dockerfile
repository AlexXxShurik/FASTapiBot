FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем FastAPI и бота
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python bot/main.py"]
