from django.urls import path

from . import views

"""
URL configuration for the dashboards app.

Defines routes for role-based dashboards:
- Editor
- Journalist
- Reader
"""

app_name = "dashboards"

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("editor/", views.dashboard, name="editor_dashboard"),
    path("journalist/", views.dashboard, name="journalist_dashboard"),
    path("reader/", views.dashboard, name="reader"),
]
