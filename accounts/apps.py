"""
accounts.apps

Module for the Accounts app configuration.

This module defines the configuration for the Accounts app, including
the default primary key field type and the app name.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the Accounts app.

    Attributes:
        default_auto_field (str): The default field type for auto-created primary keys.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
