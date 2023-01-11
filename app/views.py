from .models import Employee, Course
from .serializers import EmployeeSerializer, UserSerializer, CourseSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins, generics
# Create your views here.


# class CourseAllView(generics.ListAPIView, generics.CreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer


# shorter version of the upper defined CourseAllView class
class CourseAllView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# class CourseAllViewWithId(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer


# shorter version of the upper defined CourseAllViewWithId class
class CourseAllViewWithId(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# previous code is here
'''
class CourseAllView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # the list() method is in the ListModelMixin
    # the create() method is in the CreateModelMixin
    # the request methods are in GenericAPIView
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class CourseAllViewWithId(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
'''
