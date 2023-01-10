from .models import Employee
from django.contrib.auth.models import User
from rest_framework import serializers

# using ModelSerializer to reduce complexity


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
