from django.urls import path
from . import views

urlpatterns = [
    path('courseClassView', views.CourseAllView.as_view()),
    path('courseClassView/<int:pk>', views.CourseAllViewWithId.as_view()),
]
