from rest_framework import generics
from .serializers import InstructorSerializer, CourseSerializer
from .models import Instructor, Course
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class InstructorListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


class InstructorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()


class CourseListView(generics.ListCreateAPIView):
    # we must be logged in to the admin site to have our login data into the session
    # otherwise we will not get access to the api requested data
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
