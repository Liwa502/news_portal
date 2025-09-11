from django.apps import AppConfig

"""
Configuration for the dashboards app.
"""


class DashboardsConfig(AppConfig):
    """
    AppConfig for the Dashboards app.

    Sets the default auto field type for models.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboards"
