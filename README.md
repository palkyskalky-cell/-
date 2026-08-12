# Credit Card Default Prediction Service

**GitHub:** [https://github.com/palkyskalky-cell/credit-card-default-prediction](https://github.com/palkyskalky-cell/credit-card-default-prediction)

## Описание проекта

Сервис машинного обучения для прогнозирования дефолта по кредитным картам. Проект демонстрирует полный цикл внедрения ML-модели в production-среду: от обучения модели до организации A/B-тестирования с контейнеризацией.

### Бизнес-задача
Банк хочет автоматизировать процесс принятия решений по кредитным картам. Сервис должен прогнозировать вероятность дефолта клиента в следующем месяце на основе его кредитной истории и демографических данных.

### Ключевые возможности
- 🔮 Прогнозирование вероятности дефолта по кредитной карте
- 🐳 Контейнеризация с Docker для воспроизводимого деплоя
- 🔄 A/B-тестирование для сравнения версий моделей
- 📊 Мониторинг качества предсказаний
- 📝 Полная документация API

## Структура проекта
credit-card-default-prediction/
├── .github/ # GitHub Actions для CI/CD
├── data/ # Данные (локально, не в репозитории)
│ └── raw/ # Исходные данные
├── models/ # Сохраненные модели
│ ├── model_v1.pkl # Версия 1 модели
│ └── model_v2.pkl # Версия 2 модели (для A/B теста)
├── notebooks/ # Jupyter ноутбуки для EDA и обучения
│ ├── 01_eda.ipynb # Исследовательский анализ данных
│ └── 02_model_training.ipynb # Обучение моделей
├── src/ # Исходный код
│ ├── app/ # Веб-сервис
│ │ ├── init.py
│ │ ├── api.py # Flask эндпоинты
│ │ └── config.py # Конфигурации
│ ├── models/ # Модули для работы с моделями
│ │ ├── init.py
│ │ ├── model_loader.py # Загрузка моделей
│ │ └── predictor.py # Инференс
│ └── utils/ # Утилиты
│ ├── init.py
│ └── logger.py # Настройка логирования
├── tests/ # Тесты
│ ├── test_api.py
│ └── test_model.py
├── docker/ # Docker файлы
│ └── Dockerfile
├── scripts/ # Вспомогательные скрипты
│ ├── download_data.py
│ └── train_model.py # Скрипт обучения модели
├── docs/ # Документация
│ ├── ARCHITECTURE.md # Архитектурные решения
│ └── AB_TEST_PLAN.md # План A/B тестирования
├── screenshots/ # Скриншоты для демонстрации
│ ├── training_results.png
│ ├── health_check.png
│ ├── prediction_response.png
│ ├── ab_testing_v1.png
│ └── ab_testing_v2.png
├── requirements.txt # Зависимости Python
├── docker-compose.yml # Docker Compose (опционально)
├── .env.example # Пример переменных окружения
└── README.md # Этот файл


## Технологический стек

- **ML**: scikit-learn, pandas, numpy
- **API**: Flask
- **Контейнеризация**: Docker, Docker Compose
- **Версионирование**: Git, GitHub
- **Формат модели**: pickle / joblib

## Быстрый старт

### Предварительные требования

- Python 3.8+
- pip
- Git
- Docker (опционально)

### Локальный запуск (Windows)

1. **Клонировать репозиторий**
```bash
git clone https://github.com/palkyskalky-cell/credit-card-default-prediction.git
cd credit-card-default-prediction
2.Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate
3.Установить зависимости

pip install -r requirements.txt
4.Обучить модель
python scripts\train_model.py
5.Запустить сервис
python src\app\api.py
Сервис будет доступен по адресу: http://localhost:5000
Запуск через Docker
1.Собрать образ
docker build -t credit-card-prediction:latest -f docker/Dockerfile .
2.Запустить контейнер
docker run -p 5000:5000 credit-card-prediction:latest
3.Или использовать Docker Compose
docker-compose up -d
API Документация
Health Check
Endpoint: GET /health

Response:
{
    "status": "healthy",
    "model_loaded": true,
    "model_version": "v1",
    "timestamp": "2026-08-12T18:36:43Z"
}
Прогнозирование
Endpoint: POST /predict
{
    "features": {
        "LIMIT_BAL": 50000,
        "SEX": 1,
        "EDUCATION": 2,
        "MARRIAGE": 1,
        "AGE": 35,
        "PAY_0": 0,
        "PAY_2": 0,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": 0,
        "PAY_6": 0,
        "BILL_AMT1": 3000,
        "BILL_AMT2": 2500,
        "BILL_AMT3": 2200,
        "BILL_AMT4": 2000,
        "BILL_AMT5": 1800,
        "BILL_AMT6": 1500,
        "PAY_AMT1": 500,
        "PAY_AMT2": 400,
        "PAY_AMT3": 350,
        "PAY_AMT4": 300,
        "PAY_AMT5": 250,
        "PAY_AMT6": 200
    }
}
Response:
{
    "prediction": 0,
    "probability": 0.23,
    "model_version": "v1",
    "timestamp": "2026-08-12T18:25:19Z",
    "processing_time_ms": 195.07
}
Примеры curl-запросов
Health Check:
curl -X GET http://localhost:5000/health
Prediction:
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"features\": {\"LIMIT_BAL\": 50000, \"SEX\": 1, \"EDUCATION\": 2, \"MARRIAGE\": 1, \"AGE\": 35, \"PAY_0\": 0, \"PAY_2\": 0, \"PAY_3\": 0, \"PAY_4\": 0, \"PAY_5\": 0, \"PAY_6\": 0, \"BILL_AMT1\": 3000, \"BILL_AMT2\": 2500, \"BILL_AMT3\": 2200, \"BILL_AMT4\": 2000, \"BILL_AMT5\": 1800, \"BILL_AMT6\": 1500, \"PAY_AMT1\": 500, \"PAY_AMT2\": 400, \"PAY_AMT3\": 350, \"PAY_AMT4\": 300, \"PAY_AMT5\": 250, \"PAY_AMT6\": 200}}"
Демонстрация работы
1. Обучение модели
https://screenshots/training_results.png

2. Проверка здоровья сервиса (health check)
https://screenshots/health_check.png

3. Пример предсказания
https://screenshots/prediction_response.png

4. A/B тестирование: версия v1
https://screenshots/ab_testing_v1.png

5. A/B тестирование: версия v2
https://screenshots/ab_testing_v2.png

A/B Тестирование
Проект поддерживает A/B тестирование для сравнения двух версий модели. Подробности в AB_TEST_PLAN.md.

Основные метрики A/B теста:
F1-score для класса дефолта (основная метрика)

Precision для класса дефолта (дополнительная метрика)

Процент снижения финансовых потерь

Как протестировать:
# Запрос к версии 1 модели (control group)
curl -X POST "http://localhost:5000/predict?model_version=v1" -H "Content-Type: application/json" -d "{\"features\": {\"LIMIT_BAL\": 50000, \"SEX\": 1, \"EDUCATION\": 2, \"MARRIAGE\": 1, \"AGE\": 35, \"PAY_0\": 0, \"PAY_2\": 0, \"PAY_3\": 0, \"PAY_4\": 0, \"PAY_5\": 0, \"PAY_6\": 0, \"BILL_AMT1\": 3000, \"BILL_AMT2\": 2500, \"BILL_AMT3\": 2200, \"BILL_AMT4\": 2000, \"BILL_AMT5\": 1800, \"BILL_AMT6\": 1500, \"PAY_AMT1\": 500, \"PAY_AMT2\": 400, \"PAY_AMT3\": 350, \"PAY_AMT4\": 300, \"PAY_AMT5\": 250, \"PAY_AMT6\": 200}}"

# Запрос к версии 2 модели (test group)
curl -X POST "http://localhost:5000/predict?model_version=v2" -H "Content-Type: application/json" -d "{\"features\": {\"LIMIT_BAL\": 50000, \"SEX\": 1, \"EDUCATION\": 2, \"MARRIAGE\": 1, \"AGE\": 35, \"PAY_0\": 0, \"PAY_2\": 0, \"PAY_3\": 0, \"PAY_4\": 0, \"PAY_5\": 0, \"PAY_6\": 0, \"BILL_AMT1\": 3000, \"BILL_AMT2\": 2500, \"BILL_AMT3\": 2200, \"BILL_AMT4\": 2000, \"BILL_AMT5\": 1800, \"BILL_AMT6\": 1500, \"PAY_AMT1\": 500, \"PAY_AMT2\": 400, \"PAY_AMT3\": 350, \"PAY_AMT4\": 300, \"PAY_AMT5\": 250, \"PAY_AMT6\": 200}}"
Мониторинг и логирование
Логи записываются в формате JSON с информацией о:

Времени запроса

Версии модели

Предсказании и вероятности

Времени обработки

IP-адресе клиента

Для production рекомендуется использовать ELK-стек (Elasticsearch, Logstash, Kibana) для сбора и визуализации логов.

CI/CD Pipeline
Проект настроен с использованием GitHub Actions:

Автоматическое тестирование при push в main

Сборка Docker образа

Публикация в Docker Hub

Документация
Архитектурные решения - описание архитектуры сервиса и обоснование выбора технологий

План A/B тестирования - детальный план проведения A/B теста

MLOps концепции - описание DVC, MLflow и других инструментов

Контакты
Автор: Ирина
GitHub: palkyskalky-cell

Лицензия
MIT License

Request Body:
