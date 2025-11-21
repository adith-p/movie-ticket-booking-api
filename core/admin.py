from django.contrib import admin
from .models import Movie, Booking, Show

# Register your models here.

admin.site.register(Movie)
admin.site.register(Booking)
admin.site.register(Show)
