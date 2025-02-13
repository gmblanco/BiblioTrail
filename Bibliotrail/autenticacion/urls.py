from django.urls import path
from .views import VistaRegistro, cerrar_sesion

urlpatterns = [
    path('', VistaRegistro.as_view(),name="registro"),
    path('cerrar_sesion/',cerrar_sesion,name="cerrar_sesion"),
]