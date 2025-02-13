# admin.py
from django.contrib import admin
from .models import Products,Signup, login, Cart 
# Register your models here.


admin.site.register(Products)
admin.site.register(Signup)
admin.site.register(login)
admin.site.register(Cart)

