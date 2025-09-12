"""
articles.urls

URL configuration for the Articles app.

Defines routes for:
- Reader views
- Journalist views
- Editor views
- Publisher creation
- API endpoints for subscriber articles and newsletters
"""

from django.urls import path

from . import api_views, views

app_name = "articles"

urlpatterns = [
    # ---------------- Reader ----------------
    path("", views.home, name="home"),
    path("<int:pk>/", views.reader_article_detail, name="detail"),
    path("reader/", views.reader_article_list, name="reader_list"),
    path("<int:pk>/", views.article_detail, name="article_detail"),

    # ---------------- Editor ----------------
    path("editor/", views.editor_article_list, name="editor_list"),
    path("editor/<int:pk>/edit/", views.editor_article_edit, name="editor_edit"),
    path("editor/<int:pk>/delete/", views.editor_article_delete, name="editor_delete"),

    # ---------------- Journalist ----------------
    path(
        "journalist/create/",
        views.journalist_article_create,
        name="journalist_create",
    ),
    path("journalist/", views.journalist_article_list, name="journalist_list"),
    path(
        "journalist/<int:pk>/edit/",
        views.journalist_article_edit,
        name="journalist_edit",
    ),
    path(
        "journalist/<int:pk>/delete/",
        views.journalist_article_delete,
        name="journalist_delete",
    ),

    # ---------------- Publisher ----------------
    path("publisher/create/", views.create_publisher, name="create_publisher"),

    # ---------------- API Endpoints ----------------
    path(
        "api/articles/",
        api_views.SubscriberArticlesAPI.as_view(),
        name="api_articles",
    ),
    path(
        "api/newsletters/",
        api_views.SubscriberNewslettersAPI.as_view(),
        name="api_newsletters",
    ),
]
