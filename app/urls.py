from django.urls import path
from . import views

urlpatterns = [
    path('employees', views.employeeListView),
    path('employees/<int:pk>', views.employeeDetailView),
    path('users', views.userListView),
    # assignment
    path('courses', views.courseListView),
    path('courses/<int:pk>', views.courseDetailView),
    path('courseClassView', views.CourseAllView.as_view()),
    path('courseClassView/<int:pk>', views.CourseAllViewWithId.as_view()),
]
