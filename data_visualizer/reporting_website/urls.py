<<<<<<< HEAD
from django.contrib import admin
=======
>>>>>>> a54b7a94a1f0b74208c7a4dbcf2b6e362c95a73e
from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home),
    path('statistical', views.statistical),
=======
    path('', views.home, name='home'),
>>>>>>> a54b7a94a1f0b74208c7a4dbcf2b6e362c95a73e
]