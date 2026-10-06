from django.contrib import admin

from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "complaint",
        "inspector",
        "result",
        "created_at",
    )

    list_filter = (
        "result",
        "created_at",
    )

    search_fields = (
        "complaint__description",
        "inspector__username",
        "remarks",
    )