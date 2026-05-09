# Лабораторная работа №5: Service Discovery

## Цель работы

Реализовать динамическое обнаружение сервисов в распределённой системе с использованием Consul, адаптировав решение под научные задачи (ML-модели, датчики).

## Технологии

- **Service Discovery:** HashiCorp Consul
- **Бэкенд:** Flask + SQLAlchemy + PostgreSQL
- **Фронтенд:** React + TypeScript + Vite + Nginx
- **Контейнеризация:** Docker, Docker Compose

## Архитектура

Система состоит из четырёх сервисов:
- **consul** – реестр сервисов (UI на порту 8500)
- **db** – PostgreSQL для хранения показаний датчиков
- **backend** – REST API (Flask), регистрируется в Consul при старте
- **frontend** – React-приложение, визуализирует данные и взаимодействует с API

При запуске бэкенд автоматически отправляет запрос на регистрацию в Consul, указывая свой адрес (`backend:5000`), теги (`api`, `v1`, `ml`) и health-проверку (эндпоинт `/health`). Consul периодически проверяет доступность сервиса и исключает его при падении.

## Структура проекта
<img width="378" height="522" alt="image" src="https://github.com/user-attachments/assets/71b6c674-3b55-4d86-99b4-439ac916e1e6" />


## Запуск

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/bulochnikoff/Lab5.git
   cd Lab5

2.Запустить все сервисы:

bash
docker compose up --build

Сборка может занять несколько минут (скачиваются образы Python, Node, PostgreSQL, Consul).

3.После запуска проверить доступность:

-Frontend → http://localhost:8082

-Backend API → http://localhost:5002/health

-Consul UI → http://localhost:8500

-Swagger документация → http://localhost:5002/api/docs


Функциональность

Регистрация сервиса в Consul
При старте контейнера backend выполняется register_with_consul(), которая отправляет POST-запрос на /discovery/register c параметрами:

json
{
  "id": "backend-<hostname>",
  "address": "backend:5000",
  "tags": ["api", "v1", "ml"]
}
Consul создаёт сервис analytics-service с тегами и health check (HTTP /health).


Health check

Эндпоинт /health проверяет соединение с БД. Если проверка не проходит (или сервис недоступен), Consul помечает сервис как unhealthy и исключает из списка.

Получение списка сервисов
GET /discovery/services – все сервисы

GET /discovery/services?tag=ml – фильтрация по тегу

Фронтенд (прокси)
Nginx в контейнере фронтенда проксирует запросы /api/* на бэкенд (http://backend:5000), что позволяет обойти CORS.

Примеры запросов
Проверка здоровья бэкенда
bash
curl http://localhost:5002/health
Ответ: {"status":"ok"}

Получение всех показаний датчиков
bash
curl http://localhost:5002/api/v1/sensors/readings
Ответ: массив объектов.

Добавление показания
bash
curl -X POST http://localhost:5002/api/v1/sensors/readings \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":"123456789012345678901234567890123456","value":25.5,"timestamp":"2026-05-09T12:00:00Z","location":{"lat":55.75,"lon":37.61}}'
ML-прогноз (сумма признаков)
bash
curl -X POST http://localhost:5002/api/v1/models/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1,2,3,4]}'
Ответ: {"prediction":10, "status":"success"}

Получение зарегистрированных сервисов из Consul
bash
curl http://localhost:5002/discovery/services
Проверка работы Service Discovery
Открыть Consul UI: http://localhost:8500

В разделе "Services" должен отображаться analytics-service.

Нажать на сервис → увидеть его адрес (backend:5000), теги и статус health check.

Остановить бэкенд (docker stop lab5_backend) – через 10-20 секунд сервис станет "unhealthy" или исчезнет.

Запустить снова → сервис восстановится.

Переменные окружения
Основные настройки в docker-compose.yml:

DATABASE_URL – подключение к PostgreSQL

CONSUL_URL – адрес Consul API

SERVICE_NAME – имя сервиса в Consul (по умолчанию analytics-service)
