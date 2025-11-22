from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import (
    AllMovieSerializer,
    MovieSerializer,
    CreateBookingSerializer,
    MyBookingSerializer,
    BookingInputSerializer,
)
from .models import Movie, Booking
from .schema import responses

# Create your views here.


class GetAllMoviesApiView(generics.ListAPIView):
    """Public endpoint to list all movies."""

    queryset = Movie.objects.all()
    serializer_class = AllMovieSerializer


class MovieApiView(APIView):
    """Retrieve a single movie and its scheduled shows."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self, movie_id):
        return Movie.objects.get(pk=movie_id)

    @extend_schema(responses={200: MovieSerializer, 404: responses.movie_show_404})
    def get(self, request, movie_id):
        try:
            movie_queryset = self.get_queryset(movie_id)
        except Movie.DoesNotExist:
            return Response(
                data={"detail": f"Movie with id {movie_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = MovieSerializer(instance=movie_queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookApiView(APIView):
    """Endpoint to book a ticket for a specific show."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BookingInputSerializer,
        responses={
            400: responses.book_show_400,
            404: responses.book_show_404,
            409: responses.book_show_409,
        },
    )
    def post(self, request, show_id):
        serializer = CreateBookingSerializer(
            data=request.data,
            context={"show_id": show_id, "request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelBookingApiView(APIView):
    """Cancel a user's booking."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self, booking_id, user):
        return Booking.objects.get(pk=booking_id, user=user)

    @extend_schema(
        responses={
            200: responses.cancel_booking_200,
            404: responses.cancel_booking_404,
            409: responses.cancel_booking_409,
        }
    )
    def post(self, request, booking_id):
        try:
            booking_instance = self.get_queryset(booking_id, request.user)
        except Booking.DoesNotExist:
            return Response(
                data={
                    "details": f"booking with id {
                        booking_id} does not exist"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if booking_instance.status == "cancelled":
            return Response(
                data={"detail": "This booking is already cancelled."},
                status=status.HTTP_409_CONFLICT,
            )

        booking_instance.status = "cancelled"
        booking_instance.save()

        return Response(
            {
                "detail": "Booking cancelled successfully",
                "booking_id": booking_instance.id,
            },
            status=status.HTTP_200_OK,
        )


class MyBookingApiView(APIView):
    """List all bookings made by the currently logged-in user."""

    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MyBookingSerializer})
    def get(self, request):
        # select_related is used to avoid the multiple query and optimize for N + 1 problem
        booking_instance = Booking.objects.filter(user=request.user).select_related(
            "show", "show__movie"
        )
        serializer = MyBookingSerializer(instance=booking_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
