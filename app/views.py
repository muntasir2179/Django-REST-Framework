from django.shortcuts import render
from django.http import JsonResponse
from .models import Employee
from .serializers import EmployeeSerializer, UserSerializer
from django.contrib.auth.models import User
# Create your views here.


def employeeListView(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    # Json response takes dictionary other wise we need to set safe=False to avoid any exception
    return JsonResponse(serializer.data, safe=False)


def userListView(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
