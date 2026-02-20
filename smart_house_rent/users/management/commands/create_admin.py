from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create an admin user with specified credentials'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if admin user already exists
        if User.objects.filter(email='admin@admin.com').exists():
            self.stdout.write(
                self.style.WARNING('Admin user with email admin@admin.com already exists')
            )
            return

        # Create admin user
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@admin.com',
            password='admin123',
            user_type='admin',
            is_verified=True,
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user: {admin_user.email}'
            )
        )