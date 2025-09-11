from django.apps import AppConfig

"""
Accounts app configuration.

This module defines the configuration for the Accounts app, including
the default primary key field type and app name.
"""


class AccountsConfig(AppConfig):
    """
    Configuration for the Accounts app.

    Attributes:
        default_auto_field (str): Default field type for auto-created primary keys.
        name (str): Name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
