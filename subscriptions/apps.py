"""
Subscriptions app configuration.

This app manages user subscriptions to publishers and journalists.
It defines the AppConfig class for Django to recognize this app
and sets default behaviors such as the primary key field type.
"""

from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    """
    Configuration class for the Subscriptions app.

    Attributes:
        default_auto_field (str): Default type for auto-created primary keys.
        name (str): Name of the app used by Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"
