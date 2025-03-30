from django.urls import path
from . import views
urlpatterns = [
    path('', views.catalogo,name="Catalogo"),
    #path('libros/', views.LibroListView.as_view(), name='libros'),
    #path('misprestamos/', views.PrestamosUsuarioListView.as_view(), name='mis-prestamos'),
    path('autor/', views.detalles_autor, name='autor'),
    path('buscar/', views.buscar_libros, name='buscar-libros'),
    path("libro/", views.detalles_libro, name="detalles_libro"),
    path("autor/", views.detalles_autor, name="detalles_autor"),
    path('prestar-ejemplar/<uuid:ejemplar_id>/', views.prestar_ejemplar, name='prestar-ejemplar'),
]