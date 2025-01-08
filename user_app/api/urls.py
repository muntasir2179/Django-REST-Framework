from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('login/', view=obtain_auth_token, name='login'),
    path('register/', view=views.registration_view, name='register'),
    path('logout/', view=views.logout_view, name='logout'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
