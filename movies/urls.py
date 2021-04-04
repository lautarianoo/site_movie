from django.urls import path
from movies.views import MovieView, index, MovieDetailView, AddReview, ActorView, FilterMoviesView

urlpatterns = [
    path('movies-list/', MovieView.as_view(), name='movies-list'),
    path('movies-list/filter-yrge/', FilterMoviesView.as_view(), name='filter-yrge'),
    path('movies-list/<slug:slug>', MovieDetailView.as_view(), name='movies-detail'),
    path('movies-list/review/<int:pk>', AddReview.as_view(), name='add_review'),
    path('movies-list/actor/<str:slug>', ActorView.as_view(), name='actor_detail'),
]