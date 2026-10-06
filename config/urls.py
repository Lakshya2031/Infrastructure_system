from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


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
    path(
        "inspections/",
        include("apps.inspections.urls"),
    ),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )