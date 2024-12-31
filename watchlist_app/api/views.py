from watchlist_app.models import WatchList, StreamPlatform
from .serializers import WatchListSerializer, StreamPlatformSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


class StreamPlatformAV(APIView):
    def get(self, request):
        try:
            platform = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, many=True)  # When serializer have to go through more than one object we have to set 'many=True'
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    
    
class StreamPlatformDetailsAv(APIView):
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


class WatchListAV(APIView):
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


class MovieDetailsAV(APIView):
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
    

