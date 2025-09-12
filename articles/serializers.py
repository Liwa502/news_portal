"""
articles.serializers

Serializers module for the Articles app.

Defines serializers for Article and Newsletter models to convert
model instances into JSON format for REST API responses.
"""

from rest_framework import serializers

from newsletters.models import Newsletter
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Converts Article instances to JSON and returns user and publisher as IDs.

    Attributes:
        author (PrimaryKeyRelatedField): Read-only field returning the author's ID.
        publisher (PrimaryKeyRelatedField): Read-only field returning the publisher's ID.
    """

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    publisher = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta class for ArticleSerializer.

        Specifies the model, fields to include in serialization, and
        read-only fields.
        """

        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "is_approved",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "publisher",
            "created_at",
            "updated_at",
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.

    Converts Newsletter instances to JSON and returns user and publisher as IDs.

    Attributes:
        author (PrimaryKeyRelatedField): Read-only field returning the author's ID.
        publisher (PrimaryKeyRelatedField): Read-only field returning the publisher's ID.
    """

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    publisher = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Meta class for NewsletterSerializer.

        Specifies the model, fields to include in serialization, and
        read-only fields.
        """

        model = Newsletter
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "is_approved",
            "created_at",
        ]
        read_only_fields = ["id", "author", "publisher", "created_at"]
