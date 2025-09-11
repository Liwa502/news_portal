from django.db.models import Q
from rest_framework import generics, permissions

from newsletters.models import Newsletter
from subscriptions.models import Subscription

from .models import Article
from .serializers import ArticleSerializer, NewsletterSerializer

"""
API views for articles and newsletters.

Provides REST API endpoints for retrieving articles and newsletters
based on user subscriptions and roles (reader, journalist, editor).
"""


class SubscriberArticlesAPI(generics.ListAPIView):
    """
    API endpoint to list articles for the authenticated user.

    Readers: Articles from subscribed publishers or journalists (approved only).
    Journalists: Articles authored by the user.
    Editors: All articles.
    """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a queryset of articles according to the user's role and subscriptions.

        Returns:
            QuerySet: Filtered articles for the authenticated user.
        """
        user = self.request.user
        if user.role == "reader":
            subs_pub = Subscription.objects.filter(
                user=user, publisher__isnull=False
            ).values_list("publisher", flat=True)
            subs_jour = Subscription.objects.filter(
                user=user, journalist__isnull=False
            ).values_list("journalist", flat=True)
            return Article.objects.filter(
                Q(publisher__id__in=subs_pub) | Q(author__id__in=subs_jour),
                is_approved=True,
            ).distinct()
        elif user.role == "journalist":
            return Article.objects.filter(author=user)
        elif user.role == "editor":
            return Article.objects.all()
        return Article.objects.none()


class SubscriberNewslettersAPI(generics.ListAPIView):
    """
    API endpoint to list newsletters for the authenticated user.

    Readers: Newsletters from subscribed publishers or journalists (approved only).
    Journalists: Newsletters authored by the user.
    Editors: All newsletters.
    """

    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return a queryset of newsletters according to the user's role and subscriptions.

        Returns:
            QuerySet: Filtered newsletters for the authenticated user.
        """
        user = self.request.user
        if user.role == "reader":
            subs_pub = Subscription.objects.filter(
                user=user, publisher__isnull=False
            ).values_list("publisher", flat=True)
            subs_jour = Subscription.objects.filter(
                user=user, journalist__isnull=False
            ).values_list("journalist", flat=True)
            return Newsletter.objects.filter(
                Q(publisher__id__in=subs_pub) | Q(author__id__in=subs_jour),
                is_approved=True,
            ).distinct()
        elif user.role == "journalist":
            return Newsletter.objects.filter(author=user)
        elif user.role == "editor":
            return Newsletter.objects.all()
        return Newsletter.objects.none()
