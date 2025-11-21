from django.db import models
from django.core import validators
from datetime import timedelta
from user.models import User

# Create your models here.


class StatusChoice(models.TextChoices):
    BOOKED = "booked", "Booked"
    CANCELLED = "cancelled", "Cancelled"


class Movie(models.Model):
    title = models.CharField(max_length=150, blank=True, null=False)
    duration_minutes = models.DurationField(
        null=False,
        blank=False,
        default=0,
        validators=[validators.MinValueValidator(timedelta(minutes=1))],
    )

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="show",
    )
    screen_name = models.CharField(
        null=False,
        blank=False,
        max_length=150,
    )
    date_time = models.DateTimeField(null=False, blank=False)
    total_seat = models.IntegerField()

    def __str__(self):
        return f"{self.movie}, {self.screen_name}"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="booking",
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="booking",
    )
    status = models.CharField(
        choices=StatusChoice.choices,
        default=StatusChoice.BOOKED,
        blank=False,
        null=False,
    )
    seat_number = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.show}"
