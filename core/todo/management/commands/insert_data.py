from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from todo.models import Task
import random

class Command(BaseCommand):
    help = "inserting dummy tasks"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        fake_profile=self.fake.simple_profile()
        user = CustomUser.objects.create_user(
            username=fake_profile.get('username'),
            email=self.fake.email(),
            password="test@123456"
        )

        for _ in range(5):
            Task.objects.create(
            user=user,
            title=self.fake.paragraph(nb_sentences=1),
            completed=random.choice([True, False]),
       ) 

