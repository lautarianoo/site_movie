from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from movies.models import Movie
from .forms import ReviewForm

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