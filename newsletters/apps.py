from django.apps import AppConfig

"""
Configuration for the newsletters app.
"""


class NewslettersConfig(AppConfig):
    """
    AppConfig for the Newsletters app.

    Sets the default auto field type for models.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "newsletters"
