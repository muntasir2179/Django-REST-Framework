from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)


# assignment model
class Course(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    discount = models.BooleanField()
    duration = models.DateTimeField(auto_now=True)
    authorName = models.CharField(max_length=50)
