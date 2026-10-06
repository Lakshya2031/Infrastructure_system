from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.permissions import role_required
from apps.complaints.models import Complaint

from .forms import InspectionForm
from .models import Inspection


@login_required
@role_required("Inspector")
def inspector_complaints_view(request):

    complaints = Complaint.objects.filter(
        status=Complaint.Status.SENT_TO_INSPECTOR
    ).order_by("-created_at")

    return render(
        request,
        "inspections/inspector_complaints.html",
        {
            "complaints": complaints,
        },
    )


@login_required
@role_required("Inspector")
def inspector_complaint_detail_view(
    request,
    complaint_id,
):

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        status=Complaint.Status.SENT_TO_INSPECTOR,
    )

    return render(
        request,
        "inspections/inspector_complaint_detail.html",
        {
            "complaint": complaint,
        },
    )


@login_required
@role_required("Inspector")
def perform_inspection_view(
    request,
    complaint_id,
):

    complaint = get_object_or_404(
        Complaint,
        id=complaint_id,
        status=Complaint.Status.SENT_TO_INSPECTOR,
    )

    if request.method == "POST":

        form = InspectionForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            inspection = form.save(
                commit=False
            )

            inspection.complaint = complaint
            inspection.inspector = request.user

            if (
                inspection.result
                == Inspection.Result.CONTINUE
            ):

                complaint.status = (
                    Complaint.Status.INSPECTOR_CONTINUED
                )

                message = (
                    "Inspection completed. "
                    "Complaint has been continued."
                )

            else:

                complaint.status = (
                    Complaint.Status.INSPECTOR_REJECTED
                )

                message = (
                    "Inspection completed. "
                    "Complaint has been rejected."
                )

            inspection.save()
            complaint.save()

            messages.success(
                request,
                message,
            )

            return redirect(
                "inspections:inspector_complaints"
            )

    else:

        form = InspectionForm()

    return render(
        request,
        "inspections/perform_inspection.html",
        {
            "complaint": complaint,
            "form": form,
        },
    )