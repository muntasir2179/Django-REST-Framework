from django.urls import path
from .views import InstructorListView, CourseListView


urlpatterns = [
    path('instructors', InstructorListView.as_view()),
    path('courses', CourseListView.as_view()),
]
