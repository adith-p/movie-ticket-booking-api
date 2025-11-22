from rest_framework import serializers
from rest_framework import status
from django.db import transaction  # to do atomic transaction
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
    shows = ShowSerializer(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "duration_minutes", "shows"]


class CreateBookingSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ["user", "show", "seat_number", "status", "created_at"]
        read_only_fields = ["user", "show", "status", "created_at"]

    def create(self, validated_data):
        user_instance = self.context["request"].user
        show_id = self.context["show_id"]

        with transaction.atomic():
            try:
                show = Show.objects.select_for_update().get(pk=show_id)
            except Show.DoesNotExist:
                raise serializers.ValidationError(
                    {"details": f"show with id {show_id} does not exist"},
                    code=status.HTTP_404_NOT_FOUND,
                )

            if (
                show.total_seat < validated_data["seat_number"]
                or validated_data["seat_number"] <= 0
            ):
                raise serializers.ValidationError(
                    {"detail": f"select a valid seat range ( 0 - {
                        show.total_seat} )"},
                    code=status.HTTP_400_BAD_REQUEST,
                )

            curr_booking_count = Booking.objects.filter(
                show=show, status="booked")

            if curr_booking_count.count() >= show.total_seat:
                raise serializers.ValidationError(
                    {"detail": "sold out!"}, code=status.HTTP_409_CONFLICT
                )

            overlaping_booking = curr_booking_count.filter(
                seat_number=validated_data["seat_number"], status="booked"
            ).exists()

            if overlaping_booking:
                raise serializers.ValidationError(
                    "this seats already been booked")

            booking = Booking.objects.create(
                user=user_instance,
                show=show,
                seat_number=validated_data["seat_number"],
                status="booked",
            )

            return booking


# My booking section


class MyBookingMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "duration_minutes"]


class MyBookingShowSerializer(serializers.ModelSerializer):
    movie = MyBookingMovieSerializer(read_only=True)

    class Meta:
        model = Show
        fields = ["id",  "screen_name", "date_time", "total_seat", "movie"]


class MyBookingSerializer(serializers.ModelSerializer):
    show = MyBookingShowSerializer()

    class Meta:
        model = Booking
        fields = ["id",  "status", "seat_number", "created_at", "show"]


# Request - only serializers


class BookingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["seat_number"]
