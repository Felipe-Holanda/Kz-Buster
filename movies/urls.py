from django.urls import path
from .views import MovieViews, MovieDetailViews, MovieOrderDetailView

urlpatterns = [
    path("movies/", MovieViews.as_view()),
    path("movies/<int:movie_id>/", MovieDetailViews.as_view()),
    path("movies/<int:movie_id>/orders/", MovieOrderDetailView.as_view()),
]