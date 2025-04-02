from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('eventos/', views.eventos, name="Eventos"),
]