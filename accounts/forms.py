from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser

"""
Forms module for user-related forms.

Contains custom form classes for user creation and management,
specifically extending Django's built-in UserCreationForm.
"""


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
