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

    - Editors see the editor dashboard template.
    - Journalists see the journalist dashboard template.
    - Unauthenticated users are redirected to login.
    - Other users (e.g., readers) are redirected to the articles home page.
    """
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.user.role == "editor":
        return render(request, "dashboards/editor_dashboard.html")
    elif request.user.role == "journalist":
        return render(request, "dashboards/journalist_dashboard.html")
    else:
        return redirect("articles:home")
