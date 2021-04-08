from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserLoginForm, UserRegisterForm

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