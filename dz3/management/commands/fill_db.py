from django.core.management.base import BaseCommand
from dz3.models import Profile
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        ratio = int(options['ratio'])
        self.create_users(ratio)
    def create_users(self, ratio):
        for _ in range(ratio):
            user = Profile.objects.create(username='User {}'.format(_))
            print("Created user: ", user)
