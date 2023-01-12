from .models import Course
from .serializers import CourseSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.

class CourseViewSets(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
