from django.contrib import admin
from django.utils.safestring import mark_safe

from movies.models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #Категории на странице админки
    list_display =  ('id', 'name', 'url', )
    list_display_links = ('name', )

class ReviewInlines(admin.StackedInline):
    #Выделение отдельных блоков в админке в разделе фильмы
    model = Reviews
    extra = 0

class MovieShotsInlines(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('get_image',)
    exclude = ['description']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')

    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    #Фильмы в админке
    list_display = ('title', 'category', 'url', 'draft', 'get_poster', )
    list_filter = ('category', 'year', )
    search_fields = ('title', 'category__name', )
    inlines = [MovieShotsInlines, ReviewInlines]

    readonly_fields = ('get_poster',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    get_poster.short_description = 'Постер'

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    #отзывы на странице админки
    list_display = ('name', 'email', 'parent', 'movie', 'id', )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', )

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'ip', )

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', )


admin.site.register(RatingStar)