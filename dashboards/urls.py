from django.urls import path

from . import views

"""
URL configuration for the dashboards app.

Provides role-based dashboard routes:
- Editor
- Journalist
- Reader
"""

app_name = "dashboards"

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("editor/", views.dashboard, name="editor_dashboard"),
    path("journalist/", views.dashboard, name="journalist_dashboard"),
    path("reader/", views.dashboard, name="reader_dashboard"),
]
