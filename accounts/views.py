from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm

User = get_user_model()

"""
Views module for accounts app.

Contains views for user registration, login, and logout. 
Handles authentication, user creation, and related messages.
"""


def register(request):
    """
    Handle user registration.

    GET: Display the registration form.
    POST: Validate the form, check for duplicate usernames,
          create a new user with the selected role, and redirect to login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered registration page with the form or
                      redirect to login on successful registration.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    "This username is already taken. Please choose another one.",
                )
            else:
                user = form.save(commit=False)
                user.role = form.cleaned_data["role"]
                user.save()
                messages.success(
                    request, "Account created successfully! You can now log in."
                )
                return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    """
    Handle user login.

    GET: Display the login form.
    POST: Authenticate the user with provided credentials and
          log them in if valid, then redirect to the articles home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered login page or redirect on successful login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("articles:home")
    return render(request, "accounts/login.html")


def user_logout(request):
    """
    Log out the current user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page after logging out.
    """
    logout(request)
    return redirect("accounts:login")
