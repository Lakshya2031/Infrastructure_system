from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


urlpatterns = [

    path(
        "",
        lambda request: redirect("accounts:login"),
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),

    path(
        "complaints/",
        include("apps.complaints.urls"),
    ),

]