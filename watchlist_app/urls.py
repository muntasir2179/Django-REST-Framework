from django.urls import path
from . import views


urlpatterns = [
    path('list/', view=views.movie_list, name='movie-list'),
    path('<int:pk>/', view=views.movie_details, name='movie-details'),
]
