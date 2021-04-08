from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from contact.models import Contact
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('movies:movies-list'))
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        return render(request, 'users/register_done.html', {'new_user': new_user})
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:movies-list'))

def settings_view(request):
    if request.user.is_authenticated:
        user = request.user
        contacts = Contact.objects.all().values()
        for contact in contacts:
            if user.email == contact['email']:
                user.send_email = True
            else:
                continue
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.name = data['name']
                user.movie_categories = data['movie_categories']
                user.send_email = data['send_email']
                user.save()
                return HttpResponseRedirect(reverse('movies:movies-list'))
        form = UserUpdateForm(initial={'name': user.name, 'movie_categories': user.movie_categories, 'send_email': user.send_email})
        return render(request, 'users/update.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('users:login'))
