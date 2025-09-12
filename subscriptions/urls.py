"""
URL configuration for the Subscriptions app.

Defines routes for subscribing and unsubscribing to publishers and journalists.
"""

from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    # Publisher subscription URLs
    path(
        "publisher/<int:pk>/subscribe/",
        views.subscribe_publisher,
        name="publisher_subscriber",
    ),
    path(
        "publisher/<int:pk>/unsubscribe/",
        views.unsubscribe_publisher,
        name="publisher_unsubscriber",
    ),
    # Journalist subscription URLs
    path(
        "journalist/<int:pk>/subscribe/",
        views.subscribe_journalist,
        name="journalist_subscriber",
    ),
    path(
        "journalist/<int:pk>/unsubscribe/",
        views.unsubscribe_journalist,
        name="journalist_unsubscriber",
    ),
]
