from .models import Employee
from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=12)
