from django.core.management import BaseCommand
from user.models import User
from core.models import Movie, Show
from faker import Faker
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = "management command to seed the db"

    def handle(self, *args, **options):
        faker = Faker()
        admin_instance = User.objects.create(
            is_superuser=True,
            username=faker.user_name(),
            is_active=True,
        )
        admin_instance.set_password("admin")
        admin_instance.save()

        # create movie entry
        movie_instance = Movie.objects.create(
            title="movie1", duration_minutes=timedelta(minutes=30)
        )

        screen_name = ["sr1", "sr2", "sr3"]
        # create shows
        for _ in range(5):
            Show.objects.create(
                movie=movie_instance,
                screen_name=random.choice(screen_name),
                date_time=datetime.now(),
                total_seat=random.randint(5, 20),
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
