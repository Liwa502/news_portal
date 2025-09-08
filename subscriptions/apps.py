"""
Configuration for the subscriptions app.

This app manages user subscriptions to publishers and journalists.
"""

from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    """
    AppConfig for the subscriptions app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"
