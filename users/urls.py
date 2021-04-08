from django.urls import path
from .views import login_view, register_view, logout_view, settings_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('update/', settings_view, name='update'),
]