from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from subscriptions.models import Subscription

from .forms import NewsletterForm
from .models import Newsletter

"""
Views for the newsletters app.

Includes views for editors, journalists, and readers:
- Editors: review and approve newsletters
- Journalists: create and list their newsletters
- Readers: list and view approved newsletters they are subscribed to
"""


# ---------------------------- Editor Views ----------------------------


def editor_newsletter_list(request):
    """
    Display a list of all newsletters for editors.

    Only accessible to users with the 'editor' role.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    newsletters = Newsletter.objects.all().order_by("-created_at")
    return render(
        request,
        "newsletters/editor_newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def editor_newsletter_delete(request, pk):
    """
    Allow editors to delete any newsletter.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        newsletter.delete()
        return redirect("newsletters:editor_list")
    return render(
        request,
        "newsletters/newsletter_confirm_delete.html",
        {"newsletter": newsletter},
    )


def editor_newsletter_edit(request, pk):
    """
    Allow editors to edit and approve a newsletter.

    Parameters:
    - pk: Primary key of the newsletter to edit.

    Only accessible to users with the 'editor' role.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            if "approve" in request.POST or request.POST.get("is_approved"):
                newsletter.is_approved = True
            newsletter.save()
            return redirect("newsletters:editor_list")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(
        request,
        "newsletters/editor_newsletter_edit.html",
        {"form": form, "newsletter": newsletter},
    )


# ---------------------------- Reader Views ----------------------------


@login_required
def reader_newsletter_list(request):
    """
    Display approved newsletters for a reader based on subscriptions.

    Readers see newsletters from publishers or journalists they are subscribed to.
    """
    if request.user.role != "reader":
        raise PermissionDenied()
    subscriptions_pub = Subscription.objects.filter(
        user=request.user, publisher__isnull=False
    ).values_list("publisher_id", flat=True)
    subscriptions_jour = Subscription.objects.filter(
        user=request.user, journalist__isnull=False
    ).values_list("journalist_id", flat=True)
    newsletters = (
        Newsletter.objects.filter(
            Q(publisher__id__in=subscriptions_pub)
            | Q(author__id__in=subscriptions_jour),
            is_approved=True,
        )
        .distinct()
        .order_by("-created_at")
    )
    return render(
        request, "newsletters/reader_newsletter_list.html", {"newsletters": newsletters}
    )


@login_required
def reader_newsletter_detail(request, pk):
    """
    Display a single approved newsletter to a reader.

    Parameters:
    - pk: Primary key of the newsletter.

    Only accessible to users with the 'reader' role.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk, is_approved=True)
    if request.user.role != "reader":
        raise PermissionDenied()
    return render(
        request, "newsletters/newsletter_detail.html", {"newsletter": newsletter}
    )


# ---------------------------- Journalist Views ----------------------------


def journalist_newsletter_create(request):
    """
    Allow journalists to create a new newsletter.

    The logged-in user is automatically set as the author.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            return redirect("newsletters:journalist_list")
    else:
        form = NewsletterForm()
    return render(request, "newsletters/newsletter_form.html", {"form": form})


def journalist_newsletter_list(request):
    """
    Display all newsletters created by the logged-in journalist.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    newsletters = Newsletter.objects.filter(author=request.user).order_by("-created_at")
    return render(
        request,
        "newsletters/journalist_newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def journalist_newsletter_edit(request, pk):
    """
    Allow journalists to edit their own newsletters.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    newsletter = get_object_or_404(Newsletter, pk=pk, author=request.user)
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return redirect("newsletters:journalist_list")
    else:
        form = NewsletterForm(instance=newsletter)
    return render(
        request,
        "newsletters/newsletter_form.html",
        {"form": form, "newsletter": newsletter},
    )


@login_required
def journalist_newsletter_delete(request, pk):
    """
    Allow journalists to delete their own newsletters.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    newsletter = get_object_or_404(Newsletter, pk=pk, author=request.user)
    if request.method == "POST":
        newsletter.delete()
        return redirect("newsletters:journalist_list")
    return render(
        request,
        "newsletters/newsletter_confirm_delete.html",
        {"newsletter": newsletter},
    )
