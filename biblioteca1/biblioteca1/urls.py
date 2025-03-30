from django.contrib import admin
from django.urls import path
from catalogo.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/libros/', LibroListAPIView.as_view(), name='api-libros'),
    path('api/autores/', AutorListAPIView.as_view(), name='api-autores'),
    path('api/autores/<int:pk>/', AutorDetalleAPIView.as_view(), name='api-autor-detalle'),
    path('api/libros/<int:pk>/', LibroDetalleAPIView.as_view(), name='api-libro-detalle'),
    path('api/libros/<int:libro_id>/ejemplares-disponibles/', EjemplaresDisponiblesAPIView.as_view(), name='ejemplares-disponibles'),
    path('api/ejemplares/<uuid:pk>/', EjemplarDetalleAPIView.as_view(), name='api-ejemplar-detalle'),  
    path('api/info/', BibliotecaInfoAPIView.as_view(), name='api-info-biblioteca'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)