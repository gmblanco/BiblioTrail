from django.contrib import admin
from django.urls import path
from catalogo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/libros/', LibroListAPIView.as_view(), name='api-libros'),
    path('api/libros/<int:libro_id>/ejemplares-disponibles/', EjemplaresDisponiblesAPIView.as_view(), name='ejemplares-disponibles'),
]
