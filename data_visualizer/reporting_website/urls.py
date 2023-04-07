from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('statistical', views.statistical),
    path('present', views.present),
    path('exportpdf', views.exportpdf),
    path('dummy_api', views.dummy_api)
]