from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, OpenApiExample, inline_serializer

user_signup_200 = OpenApiResponse(
    description="Created - User Created",
    response=inline_serializer(
        name="UserCreationSuccess",
        fields={"username": serializers.CharField(), "email": serializers.EmailField()},
    ),
    examples=[
        OpenApiExample(
            "Created", value={"username": "string", "email": "user@example.com"}
        )
    ],
)

user_signup_400 = OpenApiResponse(
    description="Bad Request - Validation Error",
    response=inline_serializer(
        name="UserCreationValidationErrror",
        fields={"username": serializers.CharField(), "email": serializers.EmailField()},
    ),
    examples=[
        OpenApiExample(
            "Validation Error",
            value={
                "username": ["This field is required."],
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )
    ],
)

user_signup_409 = OpenApiResponse(
    description="Conflict - Username or Email already Exist",
    response=inline_serializer(
        name="UserCreationConflict",
        fields={"username": serializers.CharField(), "email": serializers.EmailField()},
    ),
    examples=[
        OpenApiExample(
            "Confilct_Username",
            value={
                "username": "[ A user with that username already exists.]",
            },
        ),
        OpenApiExample(
            "Confilct_Email",
            value={
                "username": "[ A user with that username already exists.]",
            },
        ),
    ],
)
