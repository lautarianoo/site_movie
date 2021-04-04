from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from movies.models import Movie, Category, Actor, Genre
from .forms import ReviewForm

def index(request):
    return render(request, 'movies/index.html', {})

class GenreYears:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MovieView(GenreYears, ListView):
    #Список фильмов
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'


class MovieDetailView(GenreYears, DetailView):
    #Детализация фильмов
    model = Movie
    slug_field = 'url'
    template_name = 'movies/movies_detail.html'

class AddReview(View):
    #Отзывы
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorView(GenreYears, DetailView):
    #Вывод информации об актёре
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'

class FilterMoviesView(GenreYears, ListView):
    '''Фильтр фильмов'''
    template_name = 'movies/movies.html'
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset


