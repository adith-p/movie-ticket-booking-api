from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path(
        "login",
        TokenObtainPairView.as_view(),
        name="login_in",
    ),
    path(
        "signup",
        views.SignUpApiView.as_view(),
        name="sign_up",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
