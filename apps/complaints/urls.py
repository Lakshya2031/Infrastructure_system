from django.urls import path

from . import views


app_name = "complaints"


urlpatterns = [

    path(
        "report/",
        views.report_issue_view,
        name="report_issue",
    ),

    path(
        "my-complaints/",
        views.my_complaints_view,
        name="my_complaints",
    ),

    path(
        "supervisor/complaints/",
        views.supervisor_complaints_view,
        name="supervisor_complaints",
    ),

    path(
        "supervisor/complaints/<int:complaint_id>/",
        views.supervisor_complaint_detail_view,
        name="supervisor_complaint_detail",
    ),

    path(
        "supervisor/complaints/<int:complaint_id>/review/",
        views.supervisor_complaint_review_view,
        name="supervisor_complaint_review",
    ),

]