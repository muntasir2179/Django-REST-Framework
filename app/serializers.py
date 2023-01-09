from .models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=12)


class UserSerializer(serializers.Serializer):
    # the data we want to access, we need to define that variables in to the class
    # we need to make the variable name same as the database column names
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
