import django
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    # Session Login
    # url(r'^login/$', local_views.get_auth_token, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^auth/$',  views.user_login, name='login_form'),
    url(r'^registration/$',  views.user_registration, name='registration'),
    # url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
