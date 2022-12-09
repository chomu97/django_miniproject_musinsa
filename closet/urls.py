from django.contrib import admin
from django.urls import path
from .views import home, show_dashboard

app_name = "closet"
urlpatterns = [
    path('', home, name="home"),
    path('dashboard/', show_dashboard, name="dashboard"),

]
