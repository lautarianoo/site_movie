from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from movies.models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm

def index(request):
    return render(request, 'movies/login.html', {})

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
    paginate_by = 7
    template_name = 'movies/movies.html'

class MovieDetailView(GenreYears, DetailView):
    #Детализация фильмов
    model = Movie
    slug_field = 'url'
    template_name = 'movies/movies_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context

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
    paginate_by = 7
    template_name = 'movies/movies.html'

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class SearchFilm(GenreYears, ListView):
    '''Поиск фильмов'''
    paginate_by = 7
    template_name = 'movies/movies.html'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context

class Actorlist(GenreYears, ListView):
    model = Actor
    queryset = Actor.objects.all()
    paginate_by = 8
    template_name = 'movies/actor_list.html'

class SearchActor(GenreYears, ListView):
    '''Поиск актёров'''
    paginate_by = 8
    template_name = 'movies/actor_list.html'

    def get_queryset(self):
        return Actor.objects.filter(name__icontains=self.request.GET.get('actor'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['actor'] = f"actor={self.request.GET.get('actor')}&"
        return context


