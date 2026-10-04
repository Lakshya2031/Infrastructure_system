from django.core.management.base import BaseCommand

from apps.accounts.models import Role


ROLES = [
    {
        "name": "Citizen",
        "description": (
            "Reports public infrastructure issues "
            "and tracks their resolution."
        ),
    },
    {
        "name": "Supervisor",
        "description": (
            "Reviews complaints and assigns technicians."
        ),
    },
    {
        "name": "Technician",
        "description": (
            "Performs field repairs and updates work orders."
        ),
    },
    {
        "name": "Inspector",
        "description": (
            "Performs complaint verification and final quality assurance."
        ),
    },
    {
        "name": "Administrator",
        "description": (
            "Manages users, roles and system configuration."
        ),
    },
]


class Command(BaseCommand):

    help = "Create the default system roles."

    def handle(self, *args, **options):

        for role_data in ROLES:

            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={
                    "description": role_data["description"],
                },
            )

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created role: {role.name}"
                    )
                )

            else:

                self.stdout.write(
                    f"Role already exists: {role.name}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Role initialization completed."
            )
        )