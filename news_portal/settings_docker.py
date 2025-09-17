import os
from .settings import *
from .settings import BASE_DIR

# ----------------------------
# Database Configuration
# ----------------------------
# Here we override or define the DATABASES setting to use SQLite.
# SQLite is a lightweight, file-based database, suitable for development
# and testing purposes. For production, a more robust database like
# PostgreSQL or MySQL is recommended.

RUNNING_IN_DOCKER = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB", "news_portal"),
        "USER": os.getenv("MYSQL_USER", "user1"),
        "PASSWORD": os.getenv("DB_PASSWORD", "StrongPassword123"),
        "HOST": os.getenv("DOCKER_DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
