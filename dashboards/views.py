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

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse or HttpResponseRedirect: Dashboard template render or redirect.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.user.role == "editor":
        return render(request, "dashboards/editor_dashboard.html")
    elif request.user.role == "journalist":
        return render(request, "dashboards/journalist_dashboard.html")
    else:
        return redirect("articles:home")
