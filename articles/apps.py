from django.apps import AppConfig

"""
Articles app configuration module.

Defines the configuration for the articles app, including the default
primary key field type and app name. Also imports signals on app ready.
"""


class ArticlesConfig(AppConfig):
    """
    Configuration class for the articles app.

    Attributes:
        default_auto_field (str): Default field type for auto-created primary keys.
        name (str): Name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"

    def ready(self):
        """
        Called when the app is ready.

        Imports the articles.signals module to connect signal handlers.
        """
        import articles.signals  # noqa: F401
