from django import forms

from .models import Article

"""
Forms module for the articles app.

Contains form classes for creating and updating articles, 
including custom widgets for better UI/UX.
"""


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating Article instances.

    Uses custom widgets for title, content, publisher, author, and approval status
    to enhance form presentation and usability.

    Meta:
        model (Article): The Article model linked to this form.
        fields (list): Fields to include in the form.
        widgets (dict): Custom widgets for form fields.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher", "author", "is_approved"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter article title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write the article content here...",
                }
            ),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "author": forms.Select(attrs={"class": "form-select"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
