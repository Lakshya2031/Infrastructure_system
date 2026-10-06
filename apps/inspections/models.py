from django.conf import settings
from django.db import models

from apps.complaints.models import Complaint


class Inspection(models.Model):

    class Result(models.TextChoices):
        CONTINUE = "continue", "Continue"
        REJECT = "reject", "Reject"

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name="inspections",
    )

    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inspections",
    )

    result = models.CharField(
        max_length=20,
        choices=Result.choices,
    )

    remarks = models.TextField()

    evidence = models.FileField(
        upload_to="inspections/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Inspection #{self.pk} - Complaint #{self.complaint.pk}"