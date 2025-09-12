from django.shortcuts import redirect, render

"""
Views module for the dashboards app.

Provides role-based dashboard views for:
- Editors
- Journalists
- Readers (redirects to articles home)
"""


def dashboard(request):
    """
    Render the appropriate dashboard based on the logged-in user's role.

    Behavior:
        - Editors: Render the editor dashboard template.
        - Journalists: Render the journalist dashboard template.
        - Readers: Redirect to the articles home page.
        - Unauthenticated users: Redirect to the login page.
        - Unknown roles: Redirect to the articles home page as a fallback.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse or HttpResponseRedirect: Dashboard template render or redirect.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    role = getattr(request.user, "role", None)

    if role == "editor":
        return render(request, "dashboards/editor_dashboard.html")
    elif role == "journalist":
        return render(request, "dashboards/journalist_dashboard.html")
    elif role == "reader":
        return redirect("articles:home")
    else:
        # Fallback for unexpected roles
        return redirect("articles:home")
