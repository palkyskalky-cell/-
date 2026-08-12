# docker/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код и модель
COPY src/ ./src/
COPY models/ ./models/
COPY .env .env

# Открываем порт
EXPOSE 5000

# Запускаем сервис
CMD ["python", "src/app/api.py"]