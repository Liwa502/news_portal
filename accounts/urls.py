"""
accounts.urls

Module for the Accounts app URL configuration.

Maps URLs for user registration, login, and logout to their respective views.

Attributes:
    app_name (str): Namespace for the accounts app URLs.
    urlpatterns (list): List of URL patterns for the accounts app.
"""

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # URL for user registration
    path("register/", views.register, name="register"),
    # URL for user login
    path("login/", views.user_login, name="login"),
    # URL for user logout
    path("logout/", views.user_logout, name="logout"),
]
