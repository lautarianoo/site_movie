from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from movies.models import Movie

def index(request):
    return render(request, 'movies/index.html', {})

class MovieView(ListView):
    #Список фильмов
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'

class MovieDetailView(DetailView):
    #Детализация фильмов
    model = Movie
    slug_field = 'url'
    template_name = 'movies/movies_detail.html'