from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import generic
from rest_framework.authtoken.models import Token


def index(request):
    return render(request, 'users/index.html')


@login_required
def home(request):
    return render(request, 'users/home.html')


@login_required
def all_users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users/all_users.html', context)


@login_required
def user_details(request):

    user = User.objects.get(username=request.user.username)
    token = Token.objects.get_or_create(user=user)
    context = {'user': user,
               'token': token[0].key}
    return render(request, 'users/user_details.html', context)


