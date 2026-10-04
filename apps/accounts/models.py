from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """
    Represents a role in the Public Infrastructure
    Issue Resolution System.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model for the system.
    """

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.username

    @property
    def role_name(self):
        if self.role:
            return self.role.name.lower()

        return None

    def has_role(self, role_name):
        if not self.role:
            return False

        return self.role.name.lower() == role_name.lower()