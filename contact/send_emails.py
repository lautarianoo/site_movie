import ast
import os
import sys
import datetime
import time

from django.core.mail import EmailMultiAlternatives

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'site_movie.settings'
import django
django.setup()
from contact.models import Contact
from movies.models import Movie, Genre
from site_movie.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Новый фильм на сайте КиноВселенной! {today}'
text_content = 'Вышел новый фильм на сайте'
from_email = EMAIL_HOST_USER
html = ''
User = get_user_model()

qs = User.objects.filter(send_email=True).values()
users_dct = {}
for q in qs:
    if q['genres_id']:
        genres = Genre.objects.get(id=q['genres_id'])
        movies = Movie.objects.filter(genres=genres, timestamp=today).values()
        for movie in movies:
            html += f'<div><h3><img href="{ movie["poster"] }">{ movie["title"] }</h3><h5 align="right">{ movie["tagline"] }</h5></div>'
            html += f'<p>{movie["description"]}</p>'
            html += f'<p>{movie["year"]}</p><br>'
        if q['send_email'] == True:
            to = q['email']
            time.sleep(2)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html, "text/html")
            msg.send()
