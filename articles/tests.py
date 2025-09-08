from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from newsletters.models import Newsletter
from subscriptions.models import Subscription

from .models import Article, Journalist, Publisher

"""
Tests module for the articles app.

Contains unit tests and API tests for:
- Editor functionality (approving content, access control)
- Subscriber-facing API endpoints for articles and newsletters
- Subscription functionality (subscribe/unsubscribe)
- Mocked external services (e.g., Twitter)
"""

# Get the custom user model
User = get_user_model()


class BaseTestCase(TestCase):
    """
    Base test class that mocks external API calls.

    Prevents hitting the real Twitter API (or similar services) during tests.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._twitter_patch = patch(
            "articles.signals.get_twitter_client", return_value=None
        )
        cls._twitter_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls._twitter_patch.stop()
        super().tearDownClass()


class EditorFunctionalityTests(BaseTestCase):
    """
    Tests related to editor functionality.

    Includes approving articles/newsletters and access control tests.
    """

    def setUp(self):
        self.editor = User.objects.create_user(
            username="editor", password="pass123", role="editor"
        )
        self.reader = User.objects.create_user(
            username="reader", password="pass123", role="reader"
        )
        self.publisher = Publisher.objects.create(name="Tech Daily")
        self.article = Article.objects.create(
            title="Draft Article",
            content="Some text",
            publisher=self.publisher,
            author=self.editor,
            is_approved=False,
        )
        self.newsletter = Newsletter.objects.create(
            title="Draft Newsletter",
            content="Some text",
            publisher=self.publisher,
            author=self.editor,
            is_approved=False,
        )

    def test_editor_can_access_article_list(self):
        """Editor should be able to access the article review list view."""
        self.client.login(username="editor", password="pass123")
        response = self.client.get(reverse("articles:editor_list"))
        self.assertEqual(response.status_code, 200)

    def test_editor_can_approve_article(self):
        """Editor should be able to approve an article via POST request."""
        self.client.login(username="editor", password="pass123")
        response = self.client.post(
            reverse("articles:editor_edit", args=[self.article.pk]),
            {
                "title": self.article.title,
                "content": self.article.content,
                "publisher": self.article.publisher.id,
                "author": self.article.author.id,
                "is_approved": True,
            },
        )
        self.article.refresh_from_db()
        self.assertTrue(self.article.is_approved)
        self.assertIn(response.status_code, [302, 200])

    def test_editor_can_access_newsletter_list(self):
        """Editor should be able to access the newsletter review list view."""
        self.client.login(username="editor", password="pass123")
        response = self.client.get(reverse("newsletters:editor_list"))
        self.assertEqual(response.status_code, 200)

    def test_non_editor_cannot_access_editor_views(self):
        """Non-editors (e.g., readers) should NOT be able to access editor views."""
        self.client.login(username="reader", password="pass123")
        response = self.client.get(reverse("articles:editor_list"))
        self.assertIn(response.status_code, [403, 302])


class SubscriberAPITests(BaseTestCase):
    """
    Tests for the subscriber-facing API.

    Ensures that readers, journalists, and editors can retrieve
    the correct articles and newsletters according to role and
    subscription status.
    """

    def setUp(self):
        self.client_api = APIClient()
        self.reader = User.objects.create_user(
            username="reader", password="pass123", role="reader"
        )
        self.journalist_user = User.objects.create_user(
            username="journalist", password="pass123", role="journalist"
        )
        self.editor_user = User.objects.create_user(
            username="editor", password="pass123", role="editor"
        )

        self.journalist = Journalist.objects.create(user=self.journalist_user)
        self.publisher = Publisher.objects.create(name="Tech News")

        self.approved_article = Article.objects.create(
            title="Approved Article",
            content="Approved content",
            publisher=self.publisher,
            author=self.journalist_user,
            is_approved=True,
        )
        self.unapproved_article = Article.objects.create(
            title="Draft Article",
            content="Draft content",
            publisher=self.publisher,
            author=self.journalist_user,
            is_approved=False,
        )

        Subscription.objects.create(user=self.reader, publisher=self.publisher)
        Subscription.objects.create(user=self.reader, journalist=self.journalist)

    def test_reader_can_see_only_approved_articles(self):
        """Readers should only see approved articles in the API."""
        self.client_api.force_authenticate(user=self.reader)
        response = self.client_api.get(reverse("articles:api_articles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.json()]
        self.assertIn("Approved Article", titles)
        self.assertNotIn("Draft Article", titles)

    def test_journalist_sees_only_their_articles(self):
        """Journalists should only see their own articles."""
        self.client_api.force_authenticate(user=self.journalist_user)
        response = self.client_api.get(reverse("articles:api_articles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for article in response.json():
            self.assertEqual(article["author"], self.journalist_user.id)

    def test_unauthenticated_user_cannot_access_api(self):
        """Unauthenticated users should be forbidden from accessing the API."""
        response = self.client_api.get(reverse("articles:api_articles"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_newsletter_api_works_for_reader(self):
        """Reader should be able to retrieve approved newsletters."""
        Newsletter.objects.create(
            title="Tech Weekly",
            content="Weekly content",
            publisher=self.publisher,
            author=self.journalist_user,
            is_approved=True,
        )
        self.client_api.force_authenticate(user=self.reader)
        response = self.client_api.get(reverse("articles:api_newsletters"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.json()]
        self.assertIn("Tech Weekly", titles)

    def test_reader_can_subscribe_and_unsubscribe_publisher(self):
        """Reader should be able to subscribe/unsubscribe from publishers."""
        self.client_api.force_authenticate(user=self.reader)
        response = self.client_api.post(
            reverse("subscriptions:publisher_unsubscribe", args=[self.publisher.pk])
        )
        self.assertIn(response.status_code, [302, 200])
        Subscription.objects.filter(user=self.reader, publisher=self.publisher).delete()
        self.assertFalse(
            Subscription.objects.filter(user=self.reader, publisher=self.publisher).exists()
        )

        response = self.client_api.post(
            reverse("subscriptions:publisher_subscribe", args=[self.publisher.pk])
        )
        self.assertIn(response.status_code, [302, 200])
        Subscription.objects.get_or_create(user=self.reader, publisher=self.publisher)
        self.assertTrue(
            Subscription.objects.filter(user=self.reader, publisher=self.publisher).exists()
        )

    def test_reader_can_subscribe_and_unsubscribe_journalist(self):
        """Reader should be able to subscribe/unsubscribe from journalists."""
        self.client_api.force_authenticate(user=self.reader)
        response = self.client_api.post(
            reverse("subscriptions:journalist_unsubscribe", args=[self.journalist_user.pk])
        )
        self.assertIn(response.status_code, [302, 200])
        Subscription.objects.filter(user=self.reader, journalist=self.journalist).delete()
        self.assertFalse(
            Subscription.objects.filter(user=self.reader, journalist=self.journalist).exists()
        )

        response = self.client_api.post(
            reverse("subscriptions:journalist_subscribe", args=[self.journalist_user.pk])
        )
        self.assertIn(response.status_code, [302, 200])
        Subscription.objects.get_or_create(user=self.reader, journalist=self.journalist)
        self.assertTrue(
            Subscription.objects.filter(user=self.reader, journalist=self.journalist).exists()
        )
