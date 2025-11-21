from django.urls import path
from . import views

urlpatterns = [
    path(
        "movies/",
        views.GetAllMoviesApiView.as_view(),
        name="list-movies",
    ),
    path(
        "movies/<movie_id>/shows/",
        views.MovieApiView.as_view(),
        name="list-show-movies",
    ),
    path(
        "shows/<show_id>/book/",
        views.BookApiView.as_view(),
        name="book-show",
    ),
]
