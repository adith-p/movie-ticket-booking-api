from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import UserSignUpSerializer
from .schema import responses


# Create your views here.


class SignUpApiView(APIView):
    """
    Public endpoint for user registration.
    """

    @extend_schema(
        request=UserSignUpSerializer,
        responses={
            201: responses.user_signup_200,
            400: responses.user_signup_400,
            409: responses.user_signup_409,
        },
    )
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            try:
                serializer.save()
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                """
                handle race condition if 2 user try to signup with same name simultaneously
                """
                return Response(
                    data={"detail": "username or email already exists"},
                    status=status.HTTP_409_CONFLICT,
                )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
