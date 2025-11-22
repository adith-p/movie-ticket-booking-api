from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer

book_show_400 = OpenApiResponse(
    description="Bad request - Validation Error",
    response=inline_serializer(
        name="BookShowValidationError", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Validation Example", value={"detail": "select a valid seat range (0-100)"}
        )
    ],
)
book_show_404 = OpenApiResponse(
    description="Not Found – Does Not Exist",
    response=inline_serializer(
        name="BookShowNotFound", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Not Found Example", value={"detail": "show with id 123 does not exist"}
        )
    ],
)
book_show_409 = OpenApiResponse(
    description="Conflict – Already Exists or Sold Out",
    response=inline_serializer(
        name="BookShowConflict", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Seat Taken",
            summary="Seat already booked",
            value={"detail": "this seats already been booked"},
        ),
        OpenApiExample(
            "Sold Out", summary="Show sold out", value={"detail": "sold out!"}
        ),
    ],
)

# Cancel booking
cancel_booking_404 = OpenApiResponse(
    description="Not Found – Does Not Exist",
    response=inline_serializer(
        name="CancelBookingNotFound", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Not Found", value={"detail": "booking with id 123 does not exist"}
        )
    ],
)

cancel_booking_409 = OpenApiResponse(
    description="Conflict – Booking Already Cancelled",
    response=inline_serializer(
        name="CancelBookingConflict", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Conflict", value={"detail": "This booking is already cancelled."}
        )
    ],
)

cancel_booking_200 = OpenApiResponse(
    description="Success – Booking Cancelled",
    response=inline_serializer(
        name="CancelBookingSuccess",
        fields={
            "detail": serializers.CharField(),
            "booking_id": serializers.IntegerField(),
        },
    ),
    examples=[
        OpenApiExample(
            "Success",
            value={
                "detail": "Booking cancelled successfully",
                "booking_id": 124,
            },
        )
    ],
)
#
movie_show_404 = OpenApiResponse(
    description="Not Found – Does Not Exist",
    response=inline_serializer(
        name="MovieShowNotFound", fields={"detail": serializers.CharField()}
    ),
    examples=[
        OpenApiExample(
            "Not Found Example", value={"detail": "Movie with id 123 does not exist"}
        )
    ],
)
