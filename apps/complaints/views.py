from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ComplaintForm
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