from django.conf import settings
from django.db import models


class Department(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="categories",
    )

    def __str__(self):
        return self.name


class Location(models.Model):

    address = models.TextField(
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    def __str__(self):
        return (
            self.address
            or f"{self.latitude}, {self.longitude}"
        )


class Complaint(models.Model):

    class Status(models.TextChoices):

        SUBMITTED = (
            "submitted",
            "Submitted",
        )

        AI_ANALYZED = (
            "ai_analyzed",
            "AI Analyzed",
        )

        SUPERVISOR_REVIEW = (
            "supervisor_review",
            "Supervisor Review",
        )

        SENT_TO_INSPECTOR = (
            "sent_to_inspector",
            "Sent to Inspector",
        )

        INSPECTOR_REJECTED = (
            "inspector_rejected",
            "Inspector Rejected",
        )

        INSPECTOR_CONTINUED = (
            "inspector_continued",
            "Inspector Continued",
        )

        ASSIGNED = (
            "assigned",
            "Assigned",
        )

        WORK_ORDER = (
            "work_order",
            "Work Order",
        )

        IN_PROGRESS = (
            "in_progress",
            "In Progress",
        )

        COMPLETED = (
            "completed",
            "Completed",
        )

        FINAL_INSPECTION = (
            "final_inspection",
            "Final Inspection",
        )

        REWORK = (
            "rework",
            "Rework",
        )

        CLOSED = (
            "closed",
            "Closed",
        )

    class Priority(models.TextChoices):

        LOW = (
            "low",
            "Low",
        )

        MEDIUM = (
            "medium",
            "Medium",
        )

        HIGH = (
            "high",
            "High",
        )

        CRITICAL = (
            "critical",
            "Critical",
        )

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
    )

    description = models.TextField()

    media = models.FileField(
        upload_to="complaints/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Complaint #{self.pk}"