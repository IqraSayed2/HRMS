from django.core.management.base import BaseCommand
from users.models import User, Role

class Command(BaseCommand):
    help = 'Sets up admin user with correct role and permissions'

    def handle(self, *args, **kwargs):
        # First ensure admin role exists
        admin_role, created = Role.objects.get_or_create(
            RoleName="admin",
            defaults={'description': 'Administrator role with full access'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created admin role'))

        # Update or create admin user
        try:
            admin_user = User.objects.get(username='admin')
            admin_user.role = admin_role
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Updated existing admin user with admin role'))
        except User.DoesNotExist:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',  # Change this password!
                role=admin_role
            )
            self.stdout.write(self.style.SUCCESS('Created new admin user with admin role'))