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

# Copy the rest of the project
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate --settings=news_portal.settings_docker --noinput && python manage.py runserver 0.0.0.0:8000 --settings=news_portal.settings_docker"]

