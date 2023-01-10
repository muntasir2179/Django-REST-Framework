from .models import Employee
from django.contrib.auth.models import User
from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=12)

    def create(self, validated_data):
        print("Create Method Called for Employee...")
        # using double astric symbol (**), we can convert data into named argument
        return Employee.objects.create(**validated_data)

    def update(self, employee, validated_data):
        newEmployee = Employee(**validated_data)
        newEmployee.id = employee.id
        newEmployee.save()
        return newEmployee


class UserSerializer(serializers.Serializer):
    # the data we want to access, we need to define that variables in to the class
    # we need to make the variable name same as the database column names
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)

    def create(self, validated_data):
        print("Create Method Called for User...")
        # passing the data as the named argument using **
        return User.objects.create(**validated_data)
