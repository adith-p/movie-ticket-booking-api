from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (
    AllMovieSerializer,
    MovieSerializer,
    CreateBookingSerializer,
    MyBookingSerializer,
)
from .models import Movie, Booking

# Create your views here.


class GetAllMoviesApiView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = AllMovieSerializer


class MovieApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, movie_id):
        return get_object_or_404(Movie, pk=movie_id)

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking_instance = get_object_or_404(Booking, pk=booking_id, user=request.user)

        if booking_instance.status == "cancelled":
            return Response(
                {"detail": "This booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        booking_instance = Booking.objects.filter(user=request.user).select_related(
            "show", "show__movie"
        )
        serializer = MyBookingSerializer(instance=booking_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
