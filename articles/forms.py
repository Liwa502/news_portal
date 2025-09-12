"""
articles.forms

Forms module for the Articles app.

Contains form classes for creating and updating articles,
including custom widgets for better UI/UX.
"""

from django import forms

from .models import Article, Publisher


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating Article instances.

    Uses custom widgets for title, content, publisher, author, and approval
    status to enhance form presentation and usability.

    Meta:
        model (Article): The Article model linked to this form.
        fields (list): Fields to include in the form.
        widgets (dict): Custom widgets for form fields.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher", "is_approved"]
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


class PublisherForm(forms.ModelForm):
    """
    Form for creating and updating Publisher instances.

    Provides custom widgets for name, editors, and journalists fields
    to improve usability.

    Meta:
        model (Publisher): The Publisher model linked to this form.
        fields (list): Fields to include in the form.
        widgets (dict): Custom widgets for form fields.
    """

    class Meta:
        model = Publisher
        fields = ["name", "editors", "journalists"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Publisher Name"}
            ),
            "editors": forms.SelectMultiple(attrs={"class": "form-select"}),
            "journalists": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
