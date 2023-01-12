from .models import Employee, Course
from .serializers import EmployeeSerializer, UserSerializer, CourseSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.viewsets import ViewSet


# Create your views here.
class CourseViewSets(ViewSet):
    def list(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def retrieve(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def destroy(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        serializer = CourseSerializer(
            Course.objects.get(pk=pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
