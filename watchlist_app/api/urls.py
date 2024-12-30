from django.urls import path
from . import views


urlpatterns = [
    path('list/', view=views.MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>/', view=views.MovieDetailsAV.as_view(), name='movie-details'),
]
