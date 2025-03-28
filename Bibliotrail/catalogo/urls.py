from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo,name="Catalogo"),
    #path('libros/', views.LibroListView.as_view(), name='libros'),
    #path('libro/<int:pk>', views.LibroDetailView.as_view(), name='detalles-libro'),
    #path('autores/', views.AutorListView.as_view(), name='autores'),
    #path('autor/<int:pk>', views.AutorDetailView.as_view(), name='detalles-autor'),
    #path('misprestamos/', views.PrestamosUsuarioListView.as_view(), name='mis-prestamos'),
    path('buscar/', views.buscar_libros, name='buscar-libros'),
]