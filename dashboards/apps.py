from django.apps import AppConfig

"""
dashboards.apps

Configuration for the Dashboards app.

Defines the AppConfig for the dashboards application, including
the default primary key field type for models.
"""


class DashboardsConfig(AppConfig):
    """
    AppConfig for the Dashboards app.

    Attributes:
        default_auto_field (str): Default field type for auto-created primary keys.
        name (str): Name of the app used by Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboards"
