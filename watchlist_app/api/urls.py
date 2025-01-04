from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# creating a router
router = DefaultRouter()

# StreamPlatformVS 
#   -> ModelViewSet class
#   -> ViewSet class
router.register('stream', viewset=views.StreamPlatformVS, basename='streamplatform')   # watch/stream   and   watch/stream/1/


urlpatterns = [
    path('list/', view=views.WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', view=views.MovieDetailsAV.as_view(), name='movie-details'),

    path('', include(router.urls)),   # this router will take care of both serving all stream platform data and an individual one
    
    path('<int:pk>/review-create', view=views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review', view=views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', view=views.ReviewDetail.as_view(), name='review-detail'),
]
