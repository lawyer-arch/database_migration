FROM python:3.13

WORKDIR /project

# Копируем pyproject.toml для кеша слоёв
COPY pyproject.toml ./

RUN pip install SQLAlchemy rich python-dotenv typer tqdm pymysql aiomysql asyncpg

# Создаём виртуальное окружение
RUN python -m venv /project/.venv

# Переменные окружения для работы в venv
ENV VIRTUAL_ENV=/project/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Устанавливаем uv и pip
RUN python -m pip install --upgrade pip

# Устанавливаем зависимости уже в venv
RUN pip install SQLAlchemy rich python-dotenv typer tqdm pymysql aiomysql asyncpg

# Копируем весь проект
COPY . .

# Точка входа (можно в docker-compose.override)
CMD ["python", "-m", "main"]


