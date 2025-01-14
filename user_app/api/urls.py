from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

from . import views


urlpatterns = [
    path('login/', view=obtain_auth_token, name='login'),
    path('register/', view=views.registration_view, name='register'),
    path('logout/', view=views.logout_view, name='logout'),
]
