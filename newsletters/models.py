from django.conf import settings
from django.db import models

"""
Models for the newsletters app.

Includes the Newsletter model representing publications associated with
publishers and authors.
"""


class Newsletter(models.Model):
    """
    Newsletter model.

    Attributes:
        title (CharField): Title of the newsletter.
        content (TextField): Body content of the newsletter.
        publisher (ForeignKey): The publisher this newsletter belongs to.
        author (ForeignKey): The user who authored the newsletter.
        is_approved (BooleanField): Flag indicating if the newsletter is approved.
        created_at (DateTimeField): Timestamp of creation.

    Related names:
        publisher.newsletters: All newsletters for a publisher.
        user.newsletters: All newsletters authored by a user.
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
        return self.title
