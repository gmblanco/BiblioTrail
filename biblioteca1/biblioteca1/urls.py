from django.contrib import admin
from django.urls import path
from catalogo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/libros/', LibroListAPIView.as_view(), name='api-libros'),
    path('api/autores/', AutorListAPIView.as_view(), name='api-autores'),
    path('api/autores/<int:pk>/', AutorDetalleAPIView.as_view(), name='api-autor-detalle'),
    path('api/libros/<int:pk>/', LibroDetalleAPIView.as_view(), name='api-libro-detalle'),
    path('api/libros/<int:libro_id>/ejemplares-disponibles/', EjemplaresDisponiblesAPIView.as_view(), name='ejemplares-disponibles'),
    path('api/ejemplares/<uuid:pk>/', EjemplarDetalleAPIView.as_view(), name='api-ejemplar-detalle'),  
]
