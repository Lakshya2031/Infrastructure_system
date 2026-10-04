from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    LoginForm,
    ProfileForm,
    RegisterForm,
)


def register_view(request):
    """
    Register a new citizen account.
    """

    if request.user.is_authenticated:
        return redirect(
            "accounts:dashboard"
        )

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Account created successfully.",
            )

            return redirect(
                "accounts:login"
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    """
    Authenticate an existing user.
    """

    if request.user.is_authenticated:
        return redirect(
            "accounts:dashboard"
        )

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user,
            )

            return redirect(
                "accounts:dashboard"
            )

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    """
    Logout the current user.
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out.",
    )

    return redirect(
        "accounts:login"
    )


@login_required
def dashboard_view(request):
    """
    Display dashboard according to user role.
    """

    role = request.user.role_name

    role_dashboards = {
        "citizen": "Citizen",
        "supervisor": "Supervisor",
        "technician": "Technician",
        "inspector": "Inspector",
        "administrator": "Administrator",
    }

    dashboard_type = role_dashboards.get(
        role,
        "User",
    )

    return render(
        request,
        "accounts/dashboard.html",
        {
            "dashboard_type": dashboard_type,
        },
    )


@login_required
def profile_view(request):
    """
    Display and update the current user's profile.
    """

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect(
                "accounts:profile"
            )

    else:

        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
        },
    )