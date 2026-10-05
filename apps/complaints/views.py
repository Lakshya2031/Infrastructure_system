from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ComplaintForm, SupervisorReviewForm
from .models import Complaint, Location

from apps.accounts.permissions import role_required


@login_required
def report_issue_view(request):
    """
    Allow a citizen to report a new infrastructure issue.
    """

    if request.method == "POST":

        form = ComplaintForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            location = Location.objects.create(
                address=form.cleaned_data["address"],
                latitude=form.cleaned_data["latitude"],
                longitude=form.cleaned_data["longitude"],
            )

            complaint = form.save(
                commit=False
            )

            complaint.citizen = request.user
            complaint.location = location

            complaint.save()

            messages.success(
                request,
                "Your issue has been reported successfully.",
            )

            return redirect(
                "complaints:my_complaints"
            )

    else:

        form = ComplaintForm()

    return render(
        request,
        "complaints/report_issue.html",
        {
            "form": form,
        },
    )


@login_required
def my_complaints_view(request):
    """
    Display complaints reported by the currently
    logged-in citizen.
    """

    complaints = Complaint.objects.filter(
        citizen=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "complaints/my_complaints.html",
        {
            "complaints": complaints,
        },
    )

@login_required
@role_required("Supervisor")
def supervisor_complaints_view(request):

    complaints = Complaint.objects.filter(
        status=Complaint.Status.SUBMITTED
    ).order_by("-created_at")

    return render(
        request,
        "complaints/supervisor_complaints.html",
        {
            "complaints": complaints,
        },
    )

@login_required
@role_required("Supervisor")
def supervisor_complaint_detail_view(request, complaint_id):

    complaint = Complaint.objects.get(
        id=complaint_id
    )

    return render(
        request,
        "complaints/supervisor_complaint_detail.html",
        {
            "complaint": complaint,
        },
    )

@login_required
@role_required("Supervisor")
def supervisor_complaint_review_view(request, complaint_id):

    complaint = Complaint.objects.get(
        id=complaint_id
    )

    if request.method == "POST":

        form = SupervisorReviewForm(
            request.POST,
            instance=complaint,
        )

        if form.is_valid():

            complaint = form.save(
                commit=False
            )

            decision = form.cleaned_data["decision"]

            if decision == "continue":

                complaint.status = (
                    Complaint.Status.SENT_TO_INSPECTOR
                )

                message = (
                    "Complaint has been forwarded "
                    "to the Inspector."
                )

            else:

                complaint.status = (
                    Complaint.Status.INSPECTOR_REJECTED
                )

                message = (
                    "Complaint has been rejected."
                )

            complaint.save()

            messages.success(
                request,
                message,
            )

            return redirect(
                "complaints:supervisor_complaint_detail",
                complaint_id=complaint.id,
            )

    else:

        form = SupervisorReviewForm(
            instance=complaint
        )

    return render(
        request,
        "complaints/supervisor_review.html",
        {
            "complaint": complaint,
            "form": form,
        },
    )