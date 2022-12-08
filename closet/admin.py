from django.contrib import admin
from .models import Category, Color, Clothes
# Register your models here.

admin.site.register([Category, Color, Clothes])