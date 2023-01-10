from django.http import JsonResponse
from .models import Employee
from .serializers import EmployeeSerializer, UserSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# Create your views here.


@csrf_exempt
def employeeListView(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        # Json response takes dictionary other wise we need to set safe=False to avoid any exception
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # POST request from Postman with some data
        # JSONParser is parsing the data from request sent by Postman
        jsonData = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=jsonData)

        # showing the data in the consol
        print(jsonData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
def userListView(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        jsonData = JSONParser().parse(request)
        serializer = UserSerializer(data=jsonData)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)
