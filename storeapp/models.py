# models.py
from django.db import models
# from .models import Products
from django.contrib.auth.models import User


# Create your models here.


class Signup(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class login(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
# categories of products



# products


class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to='uploads/products/')
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


# cart..........................................................



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
