from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):
    help = 'Creates default roles for the HRMS system'

    def handle(self, *args, **kwargs):
        roles = [
            ("admin", "Administrator role with full access"),
            ("Manager", "Department manager role"),
            ("Team Leader", "Team leader role"),
            ("Employee", "Regular employee role")
        ]

        for role_name, description in roles:
            role, created = Role.objects.get_or_create(
                RoleName=role_name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created role "{role_name}"'))
            else:
                self.stdout.write(f'Role "{role_name}" already exists')