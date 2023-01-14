from django.urls import path
from .views import InstructorListView, InstructorDetailView, CourseListView, CourseDetailView


urlpatterns = [
    path('instructors', InstructorListView.as_view()),
    path('instructors/<int:pk>', InstructorDetailView.as_view(),
         name='instructor-detail'),
    path('courses', CourseListView.as_view()),
    path('courses/<int:pk>', CourseDetailView.as_view(), name='course-detail'),
]
