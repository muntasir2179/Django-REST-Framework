from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include


urlpatterns = [
    path('login/', view=obtain_auth_token, name='login')
]
