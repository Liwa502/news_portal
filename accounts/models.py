from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

"""
Custom user model module.

Defines the CustomUser class, extending Django's AbstractUser to include
roles and automatically assign groups and permissions based on the role.
Provides properties for accessing subscribed publishers and journalists.
"""

ROLE_CHOICES = (
    ("reader", "Reader"),
    ("editor", "Editor"),
    ("journalist", "Journalist"),
)


class CustomUser(AbstractUser):
    """
    Custom user model with role support.

    Attributes:
        role (CharField): The role of the user (Reader, Editor, Journalist).

    Properties:
        subscribed_publishers (QuerySet): Publishers the user is subscribed to.
        subscribed_journalists (QuerySet): Journalists the user is subscribed to.
    """

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        """
        Save the user instance and assign group and permissions based on role.

        Readers get 'view' permissions.
        Journalists get 'add', 'view', 'change', 'delete' permissions.
        Editors get 'view', 'change', 'delete' permissions.
        """
        super().save(*args, **kwargs)

        if not self.role:
            return

        group, _ = Group.objects.get_or_create(name=self.role.capitalize())

        if self.role == "reader":
            perms = Permission.objects.filter(codename__startswith="view_")
        elif self.role == "journalist":
            perms = (
                Permission.objects.filter(codename__startswith="add_")
                | Permission.objects.filter(codename__startswith="view_")
                | Permission.objects.filter(codename__startswith="change_")
                | Permission.objects.filter(codename__startswith="delete_")
            )
        elif self.role == "editor":
            perms = (
                Permission.objects.filter(codename__startswith="view_")
                | Permission.objects.filter(codename__startswith="change_")
                | Permission.objects.filter(codename__startswith="delete_")
            )
        else:
            perms = Permission.objects.none()

        group.permissions.set(perms)
        self.groups.clear()
        self.groups.add(group)

    @property
    def subscribed_publishers(self):
        """
        Get the publishers the user is subscribed to.

        Returns:
            QuerySet: Publishers subscribed by this user.
        """
        from articles.models import Publisher

        return Publisher.objects.filter(subscribed_users__user=self)

    @property
    def subscribed_journalists(self):
        """
        Get the journalists the user is subscribed to.

        Returns:
            QuerySet: Journalists subscribed by this user.
        """
        from articles.models import Journalist

        return Journalist.objects.filter(subscribed_users__user=self)
