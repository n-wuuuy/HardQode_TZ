from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_students = models.PositiveIntegerField()
    min_students = models.PositiveIntegerField()
    started = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=256)
    video = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lesson')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=256)
    students = models.ManyToManyField(User, related_name='students', blank=True, null=True)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return self.name
