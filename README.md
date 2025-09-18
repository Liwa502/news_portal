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

# Clone the repo
git clone <your-repo-url> news_portal
cd news_portal

# -----------------------
# Option 1: Local venv
# -----------------------
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Open browser at http://localhost:8000 or http://127.0.0.1:8000
# ❌ Do NOT use http://0.0.0.0:8000

# -----------------------
# Option 2: Docker
# -----------------------
docker compose up -d --build
docker compose exec app python manage.py migrate
# Open browser at http://localhost:8000 or http://127.0.0.1:8000
docker compose logs -f app
# Stop containers when done
docker compose down
# Optional: reset DB + containers
docker compose down -v

## wait-for-db.sh Script
#!/bin/bash
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
