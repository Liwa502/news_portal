"""
Models for the subscriptions app.

Defines user subscriptions to publishers or journalists.
"""

from django.conf import settings
from django.db import models


class Subscription(models.Model):
    """
    Represents a reader's subscription to a publisher or journalist.

    Attributes:
        user (ForeignKey): The reader who subscribes.
        publisher (ForeignKey, optional): The publisher the user subscribes to.
        journalist (ForeignKey, optional): The journalist the user subscribes to.
        created_at (DateTimeField): Timestamp when the subscription was created.

    Notes:
        Each subscription must be unique for a combination of user, publisher,
        and journalist.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    publisher = models.ForeignKey(
        "articles.Publisher",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subscribed_users",
    )
    journalist = models.ForeignKey(
        "articles.Journalist",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subscribed_users",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "publisher", "journalist")
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        """
        Return a human-readable representation of the subscription.
        """
        if self.publisher:
            return (
                f"{self.user.username} subscribes to publisher "
                f"{self.publisher.name}"
            )
        if self.journalist:
            return (
                f"{self.user.username} subscribes to journalist "
                f"{self.journalist.user.username}"
            )
        return f"{self.user.username} subscription"
