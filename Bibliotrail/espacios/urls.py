from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.espacios,name="Espacios"),
    path('api/disponibilidad/', DisponibilidadEspacioAPIView.as_view(), name='disponibilidad-espacio'),
    path("calendario_espacios/", disponibilidad_matriz, name="calendario_espacios"),
    path("api/disponibilidad-general/", DisponibilidadGeneralAPIView.as_view(), name="disponibilidad_general"),
]