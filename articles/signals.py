import os

import tweepy
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser
from newsletters.models import Newsletter
from subscriptions.models import Subscription

from .models import Article

"""
Signals module for the articles app.

Handles post-save signals for Article and Newsletter models.
Sends notifications to subscribers via email and optionally posts updates to Twitter.
Includes utility functions for Twitter client authentication and notification logic.
"""


def get_twitter_client():
    """
    Returns an authenticated Tweepy client if environment variables are set.

    Checks the TWITTER_ENABLED environment variable. If not enabled or
    authentication fails, returns None.

    Returns:
        tweepy.Client or None: Authenticated Twitter client or None.
    """
    if not os.getenv("TWITTER_ENABLED"):
        return None

    try:
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
        )
        return client
    except Exception:
        return None


def notify_subscribers_and_twitter(publisher, journalist, title, content):
    """
    Notify all subscribers via email and optionally post the update to Twitter.

    Subscribers can follow either:
      - A publisher (organization)
      - A journalist (specific author)

    Args:
        publisher (Publisher): Publisher instance of the article/newsletter.
        journalist (Journalist or None): Journalist instance if applicable.
        title (str): Title of the article/newsletter.
        content (str): Content of the article/newsletter.
    """
    # ---------------- FETCH SUBSCRIBERS ----------------
    publisher_sub_ids = Subscription.objects.filter(publisher=publisher).values_list(
        "user_id", flat=True
    )

    journalist_sub_ids = []
    if journalist:
        journalist_sub_ids = Subscription.objects.filter(
            journalist=journalist
        ).values_list("user_id", flat=True)

    user_ids = set(publisher_sub_ids) | set(journalist_sub_ids)
    readers = CustomUser.objects.filter(id__in=user_ids, role="reader")

    # ---------------- EMAIL NOTIFICATIONS ----------------
    for reader in readers:
        send_mail(
            subject=f"New Publication: {title}",
            message=content[:500] + "..." if len(content) > 500 else content,
            from_email=getattr(
                settings, "DEFAULT_FROM_EMAIL", "noreply@newsportal.com"
            ),
            recipient_list=[reader.email],
            fail_silently=True,
        )

    # ---------------- TWITTER NOTIFICATION ----------------
    twitter_client = get_twitter_client()
    if twitter_client:
        tweet_text = (
            f"📰 {title} by {journalist.user.username if journalist else 'Unknown'} "
            f"via {publisher.name}\n\n{content[:200]}..."
        )
        try:
            twitter_client.create_tweet(text=tweet_text)
        except Exception as e:
            print(f"[Twitter Error] Could not tweet: {e}")


# ---------------- SIGNALS ----------------


@receiver(post_save, sender=Article)
def article_approved_handler(sender, instance, created, **kwargs):
    """
    Triggered when an Article is saved.

    If the article is approved, notify subscribers via email and optionally
    post to Twitter.

    Args:
        sender (Model): The model class.
        instance (Article): The saved article instance.
        created (bool): Whether the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if instance.is_approved:
        journalist_instance = (
            getattr(instance.author, "journalist", None)
            if instance.author.role == "journalist"
            else None
        )
        notify_subscribers_and_twitter(
            publisher=instance.publisher,
            journalist=journalist_instance,
            title=instance.title,
            content=instance.content,
        )


@receiver(post_save, sender=Newsletter)
def newsletter_approved_handler(sender, instance, created, **kwargs):
    """
    Triggered when a Newsletter is saved.

    If the newsletter is approved, notify subscribers via email and optionally
    post to Twitter.

    Args:
        sender (Model): The model class.
        instance (Newsletter): The saved newsletter instance.
        created (bool): Whether the instance was created.
        **kwargs: Additional keyword arguments.
    """
    if instance.is_approved:
        journalist_instance = (
            getattr(instance.author, "journalist", None)
            if instance.author.role == "journalist"
            else None
        )
        notify_subscribers_and_twitter(
            publisher=instance.publisher,
            journalist=journalist_instance,
            title=instance.title,
            content=instance.content,
        )
