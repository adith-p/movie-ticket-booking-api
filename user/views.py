from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError

from .models import User
from .serializers import UserSignUpSerializer

# Create your views here.


class SignUpApiView(APIView):
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
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
