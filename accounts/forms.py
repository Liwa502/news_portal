"""
accounts.forms

Module containing custom user-related forms.

This module defines form classes for user creation and management,
extending Django's built-in UserCreationForm to add additional fields
such as user roles.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user with role selection.

    Extends Django's UserCreationForm to include a 'role' field
    with choices for Reader, Journalist, or Editor.

    Attributes:
        ROLE_CHOICES (tuple): Tuple of available role options.
        role (ChoiceField): Field for selecting the user's role.
    """

    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        """
        Metadata for CustomUserCreationForm.

        Specifies the model and fields to include in the form.
        """

        model = CustomUser
        fields = ("username", "email", "role", "password1", "password2")
