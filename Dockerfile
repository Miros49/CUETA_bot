# Используем Python 3.11.7
FROM python:3.11.7

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл .env (если он не подключается отдельно)
COPY .env /app/.env

# Инициализация базы данных и запуск бота
CMD ["bash", "-c", "python database/init_db.py && python bot.py"]
