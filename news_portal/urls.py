"""
URL configuration for the news_portal project.

The `urlpatterns` list routes URLs to views. For more information, see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views
    1. Import:  from my_app import views
    2. Add a URL:  path('', views.home, name='home')
Class-based views
    1. Import:  from other_app.views import Home
    2. Add a URL:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include(("articles.urls", "articles"), namespace="articles")),  # root
    path("newsletters/", include("newsletters.urls", namespace="newsletters")),
    path("dashboards/", include("dashboards.urls", namespace="dashboards")),
    path("subscriptions/", include("subscriptions.urls", namespace="subscriptions")),
]
