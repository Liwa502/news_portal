from django.conf import settings
from django.db import models

"""
Models module for the articles app.

Defines Publisher, Article, and Journalist models with their fields, 
relationships, and string representations. Supports editor/journalist 
assignments and article management.
"""


# ----------------------------
# Publisher
# ----------------------------
class Publisher(models.Model):
    """
    Publisher model representing a publishing entity.

    Can have multiple editors and journalists assigned. Editors and journalists
    are linked to the CustomUser model.

    Attributes:
        name (CharField): Name of the publisher.
        editors (ManyToManyField): Users with editor role associated with this publisher.
        journalists (ManyToManyField): Users with journalist role associated with this publisher.
    """

    name = models.CharField(max_length=255)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="editor_publishers", blank=True
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="journalist_publishers", blank=True
    )

    def __str__(self):
        """
        Return a string representation of the Publisher.

        Returns:
            str: Name of the publisher.
        """
        return self.name


# ----------------------------
# Article
# ----------------------------
class Article(models.Model):
    """
    Article model representing a news article.

    Each article belongs to a publisher and is authored by a user. Can be
    approved or pending approval.

    Attributes:
        title (CharField): Title of the article.
        content (TextField): Content/body of the article.
        publisher (ForeignKey): Publisher associated with the article.
        author (ForeignKey): User who authored the article.
        is_approved (BooleanField): Approval status of the article.
        created_at (DateTimeField): Timestamp when the article was created.
        updated_at (DateTimeField): Timestamp when the article was last updated.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(
        "Publisher", on_delete=models.CASCADE, related_name="articles"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the Article.

        Returns:
            str: Title of the article.
        """
        return self.title


# ----------------------------
# Journalist
# ----------------------------
class Journalist(models.Model):
    """
    Journalist model linking additional info to a user.

    Each journalist is linked one-to-one with a CustomUser instance.

    Attributes:
        user (OneToOneField): User associated with this journalist profile.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return a string representation of the Journalist.

        Returns:
            str: Username of the linked user.
        """
        return self.user.username
