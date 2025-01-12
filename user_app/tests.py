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

