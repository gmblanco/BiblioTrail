from django.contrib import admin
from django.urls import path
from catalogo.views import LibroListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/libros/', LibroListAPIView.as_view(), name='api-libros'),
]
