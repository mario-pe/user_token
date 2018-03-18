import json

from django.test import TestCase, Client
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, RequestsClient, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User

from users.api_views import CreateUser, AllUsers, UserDetail
from users.serializers import UserSerializer

client = Client()
factory = APIRequestFactory()


class AllUsersEndpointTests(TestCase):
    def setUp(self):
        User.objects.create(username='testUser', email='email@wp.pl', password='123456Mp')
        User.objects.create(username='testUser1', email='email1@wp.pl', password='123456Mp')
        User.objects.create(username='testUser2', email='email2@wp.pl', password='123456Mp')
        User.objects.create(username='testUser3', email='email3@wp.pl', password='123456Mp')

    def test_get_all_user(self):
        user = User.objects.get(username='testUser')
        view = AllUsers.as_view()
        users = User.objects.all()

        request = factory.get('/users/users/')
        force_authenticate(request,
                           user=user,
                           token=user.auth_token)
        response = view(request)

        serializer = UserSerializer(users, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 4)
        self.assertEquals(response.data, serializer.data)


class RegisterUserEndpointTests(TestCase):
    def setUp(self):
        self.valid_paylod = {
            'username': 'test_user',
            'password': '123456Mp',
            'email': 'testEmail@api.pl'
        }
        self.invalid_paylod = {
            'username': '',
            'password': '123456',
            'email': 'testEmail2@api.pl'
        }

    def test_register_valid_user(self):

        response = client.put('/users/register/',
                              data=json.dumps(self.valid_paylod),
                              content_type='application/json'
                              )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_user(self):

        response = client.put('/users/register/',
                              data=json.dumps(self.invalid_paylod),
                              content_type='application/json'
                              )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserEndpointTests(TestCase):
    def setUp(self):
        self.user = {
            'username': 'test_user',
            'password': '123456',
            'email': 'testEmail@api.pl'
        }
        self.valid_paylod = {
            'password': '123456',
            'email': 'testEmail@api.pl'
        }
        self.invalid_password = {
            'password': '111111',
            'email': 'testEmail@api.pl'
        }
        self.invalid_email = {
            'password': '111111',
            'email': 'email@api.pl'
        }

    def test_login_valid(self):
        client.put('/users/register/',
                   data=json.dumps(self.user),
                   content_type='application/json'
                   )
        response = client.post('/users/login/',
                               data=json.dumps(self.valid_paylod),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_password(self):
        client.put('/users/register/',
                   data=json.dumps(self.user),
                   content_type='application/json'
                   )
        response = client.post('/users/login/',
                               data=json.dumps(self.invalid_password),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_email(self):
        client.put('/users/register/',
                   data=json.dumps(self.user),
                   content_type='application/json'
                   )
        response = client.post('http://127.0.0.1:8000/users/login/',
                               data=json.dumps(self.invalid_email),
                               content_type='application/json'
                               )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailEndpointTests(TestCase):
    def setUp(self):
        self.user_1 = {
            'username': 'test_user_1',
            'password': '123456Mp',
            'email': 'testEmail@api.pl'
        }
        self.user_2 = {
            'username': 'test_user_2',
            'password': '123456',
            'email': 'testEmail2@api.pl'
        }

    def test_current_user_info(self):
        client.put('/users/register/',
                   data=json.dumps(self.user_1),
                   content_type='application/json'
                   )
        user = User.objects.get(username='test_user_1')
        view = UserDetail.as_view()

        request = factory.get('/users/user/me/')
        force_authenticate(request,
                           user=user,
                           token=user.auth_token)

        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], 'test_user_1')
        self.assertEquals(response.data['email'], 'testEmail@api.pl')
