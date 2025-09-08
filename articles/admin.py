from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser
from newsletters.models import Newsletter
from subscriptions.models import Subscription

from .models import Article, Journalist, Publisher

"""
Admin configuration module for the articles app.

Registers models with Django admin and customizes their display, filters,
search fields, and fieldsets for easier management of users, articles,
publishers, journalists, newsletters, and subscriptions.
"""


# ----------------------
# CustomUser Admin
# ----------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for the CustomUser model.

    Displays username, email, role, and permissions in admin list view.
    Customizes fieldsets and add_fieldsets for user creation and editing.
    """
    model = CustomUser
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password", "email", "role")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


# ----------------------
# Publisher Admin
# ----------------------
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin interface for the Publisher model.

    Displays publisher name and allows assigning editors and journalists
    using a horizontal filter widget.
    """
    list_display = ("name",)
    filter_horizontal = ("editors", "journalists")


# ----------------------
# Journalist Admin
# ----------------------
@admin.register(Journalist)
class JournalistAdmin(admin.ModelAdmin):
    """
    Admin interface for the Journalist model.

    Displays linked user and allows search by username or email.
    """
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


# ----------------------
# Article Admin
# ----------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for the Article model.

    Displays article details, filters by approval status and publisher,
    and allows search by title, content, or author username.
    """
    list_display = ("title", "author", "publisher", "is_approved", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content", "author__username")


# ----------------------
# Newsletter Admin
# ----------------------
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin interface for the Newsletter model.

    Displays newsletter details, filters by approval status and publisher,
    and allows search by title, content, or author username.
    """
    list_display = ("title", "author", "publisher", "is_approved", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content", "author__username")


# ----------------------
# Subscription Admin
# ----------------------
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Subscription model.

    Displays subscription details, filters by publisher and journalist,
    and allows search by user, publisher, or journalist username.
    """
    list_display = ("user", "publisher", "journalist", "created_at")
    list_filter = ("publisher", "journalist")
    search_fields = ("user__username", "publisher__name", "journalist__user__username")
