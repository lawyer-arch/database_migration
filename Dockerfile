# 1. Базовый образ
FROM python:3.13-slim

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем файлы зависимостей
COPY pyproject.toml uv.lock* /app/

# 4. Устанавливаем uv и продовые зависимости
RUN python -m pip install --upgrade pip uv \
    && uv install --no-dev

# 5. Копируем весь проект
COPY . /app

# 6. Точка входа
CMD ["python", "-m", "main"]

