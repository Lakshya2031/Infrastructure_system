from django.urls import path

from . import views


app_name = "inspections"


urlpatterns = [

    path(
        "complaints/",
        views.inspector_complaints_view,
        name="inspector_complaints",
    ),

    path(
        "complaints/<int:complaint_id>/",
        views.inspector_complaint_detail_view,
        name="inspector_complaint_detail",
    ),

    path(
        "complaints/<int:complaint_id>/inspect/",
        views.perform_inspection_view,
        name="perform_inspection",
    ),

]