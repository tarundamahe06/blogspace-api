from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Make a user superuser by email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        try:
            user              = User.objects.get(email=email)
            user.is_staff     = True
            user.is_superuser = True
            user.save()
            self.stdout.write(f'✅ {email} is now a superuser')
        except User.DoesNotExist:
            self.stdout.write(f'❌ User {email} not found')