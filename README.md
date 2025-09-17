# 📰 Django News Portal – Capstone Project

## Project Description
This is a Django-based news portal that allows users to:
- Register, log in, and manage accounts
- Create, view, edit, and delete news articles and newsletters
- Subscribe to publishers and journalists
- Manage roles and permissions through a custom user model

Full-stack Django application using **MariaDB**, runnable via **venv** or **Docker**.

## Features
- User Roles & Permissions:
  - Reader: view articles/newsletters, subscribe to publishers/journalists
  - Editor: view, update, delete articles/newsletters
  - Journalist: create, view, update, delete articles/newsletters; can publish independently
  - Roles are mutually exclusive, with proper fields assigned
- Custom User Model:
  - Users assigned to roles/groups with permissions
  - Reader → subscriptions
  - Journalist → authored articles & newsletters
- Articles must be approved by an editor
- Publishers can have multiple editors and journalists
- Newsletters managed by journalists/editors; readers can subscribe
- Admin Dashboard for managing users, roles, articles, newsletters, subscriptions

## Configuration
Create a `.env` file in the project root:

SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=news_portal
DB_USER=user1
DB_PASSWORD=StrongPassword123
DB_HOST=db
DB_PORT=3306

## 💻 Local Development (venv)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Access app at http://127.0.0.1:8000/

## 🐳 Docker Development (MariaDB + Django)
# Build and start containers in detached mode
docker compose up -d --build
# Check containers
docker compose ps
# Apply migrations
docker compose exec app python manage.py migrate
# Watch logs / server output
docker compose logs -f app
# Access app at http://localhost:8000
# Stop containers when done
docker compose down
# Stop & remove containers + DB volume (reset)
docker compose down -v

## Docker Compose Example
services:
  db:
    image: mariadb:latest
    container_name: news_portal-db
    restart: always
    environment:
      MYSQL_DATABASE: news_portal
      MYSQL_USER: user1
      MYSQL_PASSWORD: StrongPassword123
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - '3306:3306'
    volumes:
      - news_portal_db_data:/var/lib/mysql

  app:
    build: .
    container_name: news_portal-app
    command: sh /app/wait-for-db.sh db python manage.py runserver 0.0.0.0:8000
    ports:
      - '8000:8000'
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app

volumes:
  news_portal_db_data:

## wait-for-db.sh Script
#!/bin/sh
set -e
host="$1"
shift
cmd="$@"
echo "Waiting for database at $host..."
until mysqladmin ping -h "$host" --silent; do
  echo "Database is unavailable - sleeping"
  sleep 2
done
echo "Database is up - executing command"
exec $cmd
# Make executable: chmod +x wait-for-db.sh
