from rest_framework.response import Response
from rest_framework import status, generics, viewsets, filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from .pagination import WatchListPagination

# Create your views here.


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        try:
            username = self.kwargs['username']   # we can access dynamic segment value of 'username'
        except:
            username = self.request.query_params.get('username', None)   # we can access query params like this
        
        # when we use a foreignkey field for filtering we have to specify the relational field name using double underscore '__'
        return Reviews.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]    # only authenticated users can create a review
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Reviews.objects.all()
    
    # overriding the perform_create() method for applying our custom logic
    def perform_create(self, serializer):
        pk = self.kwargs['pk']   # accessing dynamic segment (pk) value from kwargs
        watchlist = WatchList.objects.get(pk=pk)   # fetching the watchlist for witch the review is submitted
        
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        if watchlist.number_rating == 0:
            # if number of rating is zero then this is going to be the first rating
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            # if number of rating is not zero then we have to calculate the average rating
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        # each time when we create a review the review counter will be incremented
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)   # saving the review for that specific watchlist


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]    # only review owner will be granted access to all types of operations
    throttle_classes = [ScopedRateThrottle]
    # we can also use this scope into other view classes as well
    throttle_scope = 'review-detail'   # the throttle rate for this view is defined in throttle settings


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]    # only authenticated users will be able to send post and put request
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    # these two class attributes will be used to do filter operations
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']  # we need to specify the field names by which we want to filter into the 'filterset_fields'
    
    # overriding the queryset to fetch specific watchlist reviews
    def get_queryset(self):
        return Reviews.objects.filter(watchlist=self.kwargs['pk'])   # accessing dynamic segment (pk) value from kwargs


# this class now will be able to perform all the operations (create read update delete)
class StreamPlatformVS(viewsets.ModelViewSet):   # We can use ReadOnlyModelViewSet class to restrict access to our data
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
class StreamPlatformDetailsAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, data=request.data)   # passing previously stored data and new updated data through request
        
        if serializer.is_valid():   # is the data is valid then updating the record
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response({"error": "Platform data is successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    
    # # class attributes for using filters
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    
    # # class attributes for using search
    # '''
    # ^	istartswith	Starts-with search.
    # =	iexact	Exact matches.
    # $	iregex	Regex search.
    # @	search	Full-text search (Currently only supported Django's PostgreSQL backend).
    # '''
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']
    
    # class attributes for using ordering
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']
    
    pagination_class = WatchListPagination


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        try:
            movies = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movies, many=True)   # When serializer have to go through more than one object we have to set 'many=True'
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class WatchDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)   # Here we are not setting 'many=True' because serializer only have to go through one object
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)   # we need to select the exact model object that we want to update and we have to pass that into the serializer alongside the data
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie, data=request.data)   # passing previously stored data and new updated data through request
        
        if serializer.is_valid():   # is the data is valid then updating the record
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"error": "Watch list data is successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    

