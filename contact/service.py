from django.core.mail import send_mail

def send_first(user_email):
    send_mail(
        'Вы подписались на рассылку КиноВселенная',
        'Мы будем присылать самые свежие фильмы, которые появились у нас на сайте',
        'emailsenddjango@gmail.com',
        [user_email],
        fail_silently=False
    )