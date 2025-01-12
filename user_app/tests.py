from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


# Create your tests here.


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@gmail.com",
            "password": "testpassword",
            "password2": "testpassword"
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='testpassword')
    
    
    def test_login(self):
        data = {
            "username": "testcase",
            "password": "testpassword"
        }
        
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout(self):
        # we have to login and get the access token to perform logout
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # sending a logout request
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

