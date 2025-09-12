from .settings import *

# ----------------------------
# Database Configuration
# ----------------------------
# Here we override or define the DATABASES setting to use SQLite.
# SQLite is a lightweight, file-based database, suitable for development
# and testing purposes. For production, a more robust database like
# PostgreSQL or MySQL is recommended.

DATABASES = {
    'default': {
        # ENGINE specifies the backend database engine to use.
        'ENGINE': 'django.db.backends.sqlite3',

        # NAME specifies the path to the database file.
        # Using BASE_DIR / "db.sqlite3" stores the file in the project root.
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
