"""
Views for managing reader subscriptions to publishers and journalists.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect

from articles.models import Journalist, Publisher

from .models import Subscription


@login_required
def subscribe_publisher(request, pk):
    """
    Subscribe the authenticated reader to a publisher.

    Args:
        request: HttpRequest object.
        pk (int): Publisher primary key.

    Raises:
        PermissionDenied: If the user is not a reader.

    Returns:
        HttpResponseRedirect to the home page with a success message.
    """
    if request.user.role != "reader":
        raise PermissionDenied()

    publisher = get_object_or_404(Publisher, pk=pk)
    Subscription.objects.get_or_create(user=request.user, publisher=publisher)
    messages.success(request, f"Subscribed to {publisher.name}")
    return redirect("articles:home")


@login_required
def unsubscribe_publisher(request, pk):
    """
    Unsubscribe the authenticated reader from a publisher.

    Args:
        request: HttpRequest object.
        pk (int): Publisher primary key.

    Raises:
        PermissionDenied: If the user is not a reader.

    Returns:
        HttpResponseRedirect to the home page with a success message.
    """
    if request.user.role != "reader":
        raise PermissionDenied()

    publisher = get_object_or_404(Publisher, pk=pk)
    Subscription.objects.filter(user=request.user, publisher=publisher).delete()
    messages.success(request, f"Unsubscribed from {publisher.name}")
    return redirect("articles:home")


@login_required
def subscribe_journalist(request, pk):
    """
    Subscribe the authenticated reader to a journalist.

    Args:
        request: HttpRequest object.
        pk (int): Journalist primary key.

    Raises:
        PermissionDenied: If the user is not a reader.

    Returns:
        HttpResponseRedirect to the home page with a success message.
    """
    if request.user.role != "reader":
        raise PermissionDenied()

    journalist = get_object_or_404(Journalist, pk=pk)
    Subscription.objects.get_or_create(user=request.user, journalist=journalist)
    messages.success(request, f"Subscribed to {journalist.user.username}")
    return redirect("articles:home")


@login_required
def unsubscribe_journalist(request, pk):
    """
    Unsubscribe the authenticated reader from a journalist.

    Args:
        request: HttpRequest object.
        pk (int): Journalist primary key.

    Raises:
        PermissionDenied: If the user is not a reader.

    Returns:
        HttpResponseRedirect to the home page with a success message.
    """
    if request.user.role != "reader":
        raise PermissionDenied()

    journalist = get_object_or_404(Journalist, pk=pk)
    Subscription.objects.filter(user=request.user, journalist=journalist).delete()
    messages.success(request, f"Unsubscribed from {journalist.user.username}")
    return redirect("articles:home")
