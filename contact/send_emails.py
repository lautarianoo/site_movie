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
from movies.models import Movie
from site_movie.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Новый фильм на сайте КиноВселенной! {today}'
text_content = 'Вышел новый фильм на сайте'
from_email = EMAIL_HOST_USER
html = ''
qs = Contact.objects.all().values()
movies = Movie.objects.filter(timestamp=today).values()
for q in qs:
    for movie in movies:
        html += f'<div><h3><img href="{ movie["poster"] }">{ movie["title"] }</h3><h5 align="right">{ movie["tagline"] }</h5></div>'
        html += f'<p>{movie["description"]}</p>'
        html += f'<p>{movie["year"]}</p><br>'
    to = q['email']
    time.sleep(2)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html, "text/html")
    msg.send()
