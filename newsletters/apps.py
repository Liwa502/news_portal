from django.apps import AppConfig

"""
Configuration for the newsletters app.
"""


class NewslettersConfig(AppConfig):
    """
    AppConfig for the Newsletters app.

    Attributes:
        default_auto_field (str): Default field type for auto-created primary keys.
        name (str): Name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "newsletters"
