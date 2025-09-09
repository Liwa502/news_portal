from django.urls import path
from . import views

"""
URL configuration for the newsletters app.

Defines routes for newsletters by role:
- Editor: review and edit newsletters
- Journalist: create and list own newsletters
- Reader: list and view newsletters
"""

app_name = "newsletters"

urlpatterns = [
    # Editor URLs
    path("editor/", views.editor_newsletter_list, name="editor_list"),
    path("editor/<int:pk>/edit/", views.editor_newsletter_edit, name="editor_edit"),
    path("editor/<int:pk>/delete/", views.editor_newsletter_delete, name="editor_delete"),

    # Journalist URLs
    path(
        "journalist/create/",
        views.journalist_newsletter_create,
        name="journalist_create",
    ),
    path("journalist/", views.journalist_newsletter_list, name="journalist_list"),
    path("journalist/<int:pk>/edit/", views.journalist_newsletter_edit, name="journalist_edit"),
    path("journalist/<int:pk>/delete/", views.journalist_newsletter_delete, name="journalist_delete"),

    # Reader URLs
    path("reader/", views.reader_newsletter_list, name="reader_list"),
    path("reader/<int:pk>/", views.reader_newsletter_detail, name="reader_detail"),
]
