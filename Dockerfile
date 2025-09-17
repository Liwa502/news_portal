FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for mariadb/mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    mariadb-client \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Copy wait-for-db script and make it executable
COPY wait-for-db.sh /app/
RUN chmod +x /app/wait-for-db.sh

# Expose Django port
EXPOSE 8000

# Run server, waiting for DB
CMD ["sh", "/app/wait-for-db.sh", "db", "sh", "-c", "python manage.py migrate --settings=news_portal.settings_docker --noinput && python manage.py runserver 0.0.0.0:8000 --settings=news_portal.settings_docker"]

