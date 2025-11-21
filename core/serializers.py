from rest_framework import serializers
from django.shortcuts import get_object_or_404

from django.db import transaction  # to do atomic transaction
from django.db.models import Q
from user.models import User
from .models import Movie, Booking, Show


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ["id", "screen_name", "date_time", "total_seat"]
        read_only_fields = ["id"]


class AllMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    shows = ShowSerializer(source="show", many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "duration_minutes", "shows"]


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["seat_number"]
        read_only_fields = ["user", "show", "status", "created_at"]

    def create(self, validated_data):
        user_instance = self.context["request"].user
        show_id = self.context.get("show_id")

        with transaction.atomic():
            show = Show.objects.select_for_update().get(pk=show_id)
            if show.total_seat < validated_data["seat_number"]:
                raise serializers.ValidationError(
                    "seat number can't exceed total seats"
                )

            curr_booking_count = Booking.objects.filter(show=show, status="booked")

            if curr_booking_count.count() >= show.total_seat:
                raise serializers.ValidationError("sold out!")

            overlaping_booking = curr_booking_count.filter(
                seat_number=validated_data["seat_number"], status="booked"
            ).exists()

            if overlaping_booking:
                raise serializers.ValidationError("this seats already been booked")

            booking = Booking.objects.create(
                user=user_instance,
                show=show,
                seat_number=validated_data["seat_number"],
                status="booked",
            )

            return booking
