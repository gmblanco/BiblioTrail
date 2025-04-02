from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas,name="Reservas"),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
]