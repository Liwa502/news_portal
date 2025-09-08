from django import forms
from .models import Newsletter

"""
Forms for the newsletters app.

Includes forms for creating and updating Newsletter instances.
"""


class NewsletterForm(forms.ModelForm):
    """
    Form for creating or editing a Newsletter.

    Fields:
    - title: Title of the newsletter
    - content: Body content of the newsletter
    - publisher: Publisher associated with the newsletter
    - author: Author (user) of the newsletter
    - is_approved: Boolean flag indicating if approved by editor

    Widgets are customized for Bootstrap 5 styling.
    """

    class Meta:
        model = Newsletter
        fields = ["title", "content", "publisher", "author", "is_approved"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter newsletter title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write the newsletter content here...",
                }
            ),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "author": forms.Select(attrs={"class": "form-select"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
