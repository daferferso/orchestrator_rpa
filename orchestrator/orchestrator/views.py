from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.


def login_view(request):
    """
    View for user login.

    If the user is already authenticated, redirects to the tasks page.
    If not, displays the login form.
    When the form is submitted, validates the provided credentials.
    If the credentials are valid, the user is authenticated and redirected
    to the tasks page.
    If not, an error message is displayed.

    Parameters:
    - request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: HTTP response displaying the login form or redirecting
    to the tasks page.
    """
    if request.user.is_authenticated:
        return redirect(to="tasks")
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return redirect("tasks")
            else:
                msg = "Credenciales inválidos"
        else:
            msg = "Error validando el formulario"
    return render(request, "users/login.html", context={
        "form": form, "msg": msg
    })


def logout_view(request):
    """
    View for logging out users.

    Logs out the current user's session.

    Parameters:
    - request (HttpRequest): The incoming HTTP request.

    Returns:
    HttpResponse: HTTP response that logs out the user's session and redirects
    to the login page.
    """
    logout(request)
    return redirect(to='login')
