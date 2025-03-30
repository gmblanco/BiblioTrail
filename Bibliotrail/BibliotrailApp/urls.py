from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio,name="Inicio"),
    path('eventos/', views.eventos,name="Eventos"),
    path('reservas/', views.reservas,name="Reservas"),
]