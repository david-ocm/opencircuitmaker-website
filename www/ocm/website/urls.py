"""
URL configuration for ocm website.

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
