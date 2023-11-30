from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Automatically creates a superuser if one does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin@admin.net', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
