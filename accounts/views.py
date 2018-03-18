from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, UserRegistrationForm


def user_logout(request):
    logout(request)
    context = {
        'info': 'zostales wylogowany'
    }
    return render(request, 'users/index.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('users:home')
                else:
                    context = {
                        'info': 'twoje konto jest zablokowane'
                    }
                    return render(request, 'users/index.html', context)
            else:
                context = {
                    'info': 'Nieprawidlowe dane'
                }
                return render(request, 'users/index.html', context)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form})


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('users:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
