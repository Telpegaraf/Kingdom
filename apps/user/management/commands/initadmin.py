from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with username "admin" and password "admin"'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created with password "admin"'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "admin" already exists'))
