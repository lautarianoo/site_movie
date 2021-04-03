from django.urls import path
from movies.views import MovieView, index, MovieDetailView

urlpatterns = [
    path('movies-list/', MovieView.as_view(), name='movies-list'),
    path('movies-list/<slug:slug>', MovieDetailView.as_view(), name='movies-detail'),
]