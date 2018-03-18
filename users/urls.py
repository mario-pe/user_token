from django.conf.urls import url

from users import api_views
from . import views

from rest_framework.authtoken import views as rest_views

# app_name = 'users'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^user_details/$', views.user_details, name='user_details'),
    url(r'^login/$', api_views.UserLogin.as_view()),
    url(r'^register/$', api_views.CreateUser.as_view()),
    url(r'^user/me/$', api_views.UserDetail.as_view()),
    url(r'^users/$', api_views.AllUsers.as_view()),
]

