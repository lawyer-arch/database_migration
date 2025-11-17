# Database Migration

**Проект Database Migration** — это утилита для переноса данных между базами данных MySQL и PostgreSQL.

Мигратор может работать как из Docker-контейнера, так и напрямую из локального виртуального окружения Python.

**Требования**:
* Docker и Docker Compose
* Python 3.13 (если планируется запуск без контейнера)
* Виртуальное окружение Python (venv)

**Установка**:
1. Клонируйте репозиторий:
```
git clone https://github.com/<your_username>/database_migration.git
cd database_migration
```
2. Создайте .env файл в корне проекта с переменными для подключения к БД:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=<mysql_user>
MYSQL_PASSWORD=<mysql_password>
MYSQL_DB=<mysql_db>

PG_HOST=localhost
PG_PORT=5432
PG_USER=<postgres_user>
PG_PASSWORD=<postgres_password>
PG_DB=<postgres_db>
```
    | спользуйте свои локальные БД для тестирования или внешние, если требуется.


3. (Опционально) Создайте виртуальное окружение для локального запуска:
```
# Установите uv, если ещё не установлен
python -m pip install --upgrade pip
python -m pip install uv

# Создаём виртуальное окружение (опционально)
python -m venv .venv
source .venv/bin/activate

# Установка зависимостей из pyproject.toml
uv install

```


### Запуск Docker
1. Сборка образов:
```
make build
```
2. Запуск всех сервисов (мигратор + локальные контейнеры БД, если нужны):
```
make up-all
```
3. Запуск только мигратора (без запуска контейнеров БД):
```
make up
```
4. Остановка всех контейнеров:
```
make down
```

### Запуск мигратора
Из контейнера Docker:
```
make migrate
```

Из локального виртуального окружения Python:
```
source .venv/bin/activate
python -m main
```
***Мигратор проверяет готовность БД, после чего запускает процесс миграции.***

### Управление логами
Логи мигратора:
```
make logs
```
Логи MySQL:
```
make logs-mysql
```
Логи PostgreSQL:
```
make logs-postgres
```

## Очистка данных
Если нужно очистить данные БД, созданные Docker-томами:
```
make clean-data
```

### Примечания

* Для тестирования мигратора можно использовать локальные БД без контейнеров.

* Если подключение к внешним БД, убедитесь, что порты открыты и доступны.

* Для изменения базы данных или пользователя — редактируйте .env.

* В Dockerfile и Makefile предусмотрена установка всех зависимостей, а мигратор запускается через python -m main.
