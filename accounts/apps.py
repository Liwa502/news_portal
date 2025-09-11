from django.apps import AppConfig

"""
Accounts app configuration module.

Defines the configuration for the accounts app, including the default
primary key field type and app name.
"""


class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts app.

    Attributes:
        default_auto_field (str): Default field type for auto-created primary keys.
        name (str): Name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
