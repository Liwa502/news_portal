from django.conf import settings
from django.db import models

"""
Models for the newsletters app.

Defines the Newsletter model representing publications associated with
publishers and authors.
"""


class Newsletter(models.Model):
    """
    Represents a newsletter publication associated with a publisher and author.

    Attributes:
        title (CharField): Title of the newsletter.
        content (TextField): Body content of the newsletter.
        publisher (ForeignKey): The publisher this newsletter belongs to.
        author (ForeignKey): The user who authored the newsletter.
        is_approved (BooleanField): Flag indicating if the newsletter is approved.
        created_at (DateTimeField): Timestamp of creation.

    Related objects:
        publisher.newsletters: All newsletters for a given publisher.
        user.newsletters: All newsletters authored by a given user.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    publisher = models.ForeignKey(
        "articles.Publisher",
        on_delete=models.CASCADE,
        related_name="newsletters",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the Newsletter.

        Returns:
            str: The title of the newsletter.
        """
        return self.title
