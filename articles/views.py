from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from newsletters.models import Newsletter
from subscriptions.models import Subscription

from .forms import ArticleForm, PublisherForm
from .models import Article, Journalist, Publisher

"""
Views module for the articles app.

Includes:
- Home view for all users
- Editor views (approve/edit articles)
- Reader views (list/detail)
- Journalist views (create/edit/delete articles)
"""

User = get_user_model()

# ---------------------------- Home View ----------------------------


def home(request):
    """
    Display home page with relevant articles, newsletters, publishers, and journalists
    depending on the user's role (editor, journalist, reader).

    - Editors see unapproved content.
    - Journalists see their own unapproved content.
    - Readers see approved content from their subscriptions.
    """
    if not request.user.is_authenticated:
        return render(
            request,
            "articles/home.html",
            {
                "articles": [],
                "newsletters": [],
                "publishers": [],
                "journalists": [],
                "subscribed_publishers": [],
                "subscribed_journalists": [],
            },
        )

    user = request.user
    articles = newsletters = publishers = journalists = []
    subscribed_publishers = subscribed_journalists = []

    if user.role == "editor":
        articles = Article.objects.filter(is_approved=False).order_by("-created_at")
        newsletters = Newsletter.objects.filter(is_approved=False).order_by(
            "-created_at"
        )
    elif user.role == "journalist":
        articles = Article.objects.filter(author=user, is_approved=False).order_by(
            "-created_at"
        )
        newsletters = Newsletter.objects.filter(
            author=user, is_approved=False
        ).order_by("-created_at")
    elif user.role == "reader":
        subscribed_publishers = Subscription.objects.filter(
            user=user, publisher__isnull=False
        ).values_list("publisher_id", flat=True)
        subscribed_journalists = Subscription.objects.filter(
            user=user, journalist__isnull=False
        ).values_list("journalist_id", flat=True)

        articles = (
            Article.objects.filter(
                Q(publisher__id__in=subscribed_publishers)
                | Q(author__id__in=subscribed_journalists),
                is_approved=True,
            )
            .distinct()
            .order_by("-created_at")
        )
        newsletters = (
            Newsletter.objects.filter(
                Q(publisher__id__in=subscribed_publishers)
                | Q(author__id__in=subscribed_journalists),
                is_approved=True,
            )
            .distinct()
            .order_by("-created_at")
        )
        publishers = Publisher.objects.all()
        journalists = Journalist.objects.all()
    else:
        raise PermissionDenied()

    return render(
        request,
        "articles/home.html",
        {
            "articles": articles,
            "newsletters": newsletters,
            "publishers": publishers,
            "journalists": journalists,
            "subscribed_publishers": subscribed_publishers,
            "subscribed_journalists": subscribed_journalists,
        },
    )


# ---------------------------- Editor + Journalist View ----------------------------


@login_required
def create_publisher(request):
    """
    Allow editors or journalists to create a new publisher.
    """
    if request.user.role not in ["editor", "journalist"]:
        raise PermissionDenied()

    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            # Ensure the current user is added automatically
            if request.user.role == "editor":
                publisher.editors.add(request.user)
            elif request.user.role == "journalist":
                publisher.journalists.add(request.user)
            publisher.save()
            return redirect("articles:home")
    else:
        form = PublisherForm()
    return render(request, "articles/publisher_form.html", {"form": form})


# ---------------------------- Editor Views ----------------------------


def editor_article_list(request):
    """
    Display all articles for editors to review.

    Only accessible by users with role 'editor'.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    articles = Article.objects.all().order_by("-created_at")
    return render(request, "articles/editor_article_list.html", {"articles": articles})


@login_required
def editor_article_delete(request, pk):
    """
    Allow an editor to delete any article.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        return redirect("articles:editor_list")
    return render(
        request,
        "articles/article_confirm_delete.html",
        {"article": article},
    )


def editor_article_edit(request, pk):
    """
    Allow editor to edit and approve an article.

    Only accessible by users with role 'editor'.
    """
    if not request.user.is_authenticated or request.user.role != "editor":
        raise PermissionDenied()
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            if "approve" in request.POST or request.POST.get("is_approved"):
                article.is_approved = True
            article.save()
            return redirect("articles:editor_list")
    else:
        form = ArticleForm(instance=article)
    return render(
        request, "articles/editor_article_edit.html", {"form": form, "article": article}
    )


# ---------------------------- Reader Views ----------------------------


@login_required
def reader_article_list(request):
    """
    Display approved articles for a reader based on their subscriptions.
    """
    if request.user.role != "reader":
        raise PermissionDenied()
    subscriptions_pub = Subscription.objects.filter(
        user=request.user, publisher__isnull=False
    ).values_list("publisher_id", flat=True)
    subscriptions_jour = Subscription.objects.filter(
        user=request.user, journalist__isnull=False
    ).values_list("journalist_id", flat=True)
    articles = (
        Article.objects.filter(
            Q(publisher__id__in=subscriptions_pub)
            | Q(author__id__in=subscriptions_jour),
            is_approved=True,
        )
        .distinct()
        .order_by("-created_at")
    )
    return render(request, "articles/reader_article_list.html", {"articles": articles})


@login_required
def reader_article_detail(request, pk):
    """
    Display a single approved article for a reader.
    """
    article = get_object_or_404(Article, pk=pk, is_approved=True)
    if request.user.role != "reader":
        raise PermissionDenied()
    return render(request, "articles/article_detail.html", {"article": article})


def article_detail(request, pk):
    """
    Display a single article regardless of approval status.
    """
    article = get_object_or_404(Article, pk=pk)
    return render(request, "articles/article_detail.html", {"article": article})


# ---------------------------- Journalist Views ----------------------------


def journalist_article_create(request):
    """
    Allow a journalist to create a new article.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("articles:journalist_list")
    else:
        form = ArticleForm()
    return render(request, "articles/article_form.html", {"form": form})


def journalist_article_list(request):
    """
    Display all articles created by the logged-in journalist.
    """
    if not request.user.is_authenticated or request.user.role != "journalist":
        raise PermissionDenied()
    articles = Article.objects.filter(author=request.user).order_by("-created_at")
    return render(
        request, "articles/journalist_article_list.html", {"articles": articles}
    )


def journalist_article_edit(request, pk):
    """
    Allow a journalist to edit one of their own articles.
    """
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("articles:journalist_list")
    else:
        form = ArticleForm(instance=article)
    return render(request, "articles/article_form.html", {"form": form})


def journalist_article_delete(request, pk):
    """
    Allow a journalist to delete one of their own articles.
    """
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == "POST":
        article.delete()
        return redirect("articles:journalist_list")
    return render(request, "articles/article_confirm_delete.html", {"article": article})
