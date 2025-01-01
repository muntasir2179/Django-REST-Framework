from django.urls import path
from . import views


urlpatterns = [
    path('list/', view=views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', view=views.MovieDetailsAV.as_view(), name='movie-details'),
    path('stream/', view=views.StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>/', view=views.StreamPlatformDetailsAv.as_view(), name='stream-details'),
    path('review', view=views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', view=views.ReviewDetail.as_view(), name='review-detail'),
]
