# Имя проекта
PROJECT_NAME := database_migration

# Контейнеры Docker Compose
COMPOSE := docker-compose -f docker-compose.yml

# ---------------------------------------------------
# Сборка образов
build:
	$(COMPOSE) build

# Запуск мигратора (в фоне)
up:
	$(COMPOSE) up -d migrator

# Запуск всех сервисов (в фоне)
up-all:
	$(COMPOSE) up -d

# Остановка всех контейнеров
down:
	$(COMPOSE) down

# Просмотр логов мигратора (реальное время)
logs:
	$(COMPOSE) logs -f migrator

# Просмотр логов MySQL
logs-mysql:
	$(COMPOSE) logs -f mysql

# Просмотр логов Postgres
logs-postgres:
	$(COMPOSE) logs -f postgres

# Пересборка образов и запуск всех сервисов
rebuild: down build up-all

# Очистка данных баз данных
clean-data:
	docker volume rm $(PROJECT_NAME)_mysql_data
	docker volume rm $(PROJECT_NAME)_pg_data

# Выполнение мигратора вручную в контейнере
migrate:
	$(COMPOSE) run --rm migrator
