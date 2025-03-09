from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRutas),
    path('libros/',views.getLibros),
    path('autores/',views.getAutores),
    path('ejemplares/',views.getEjemplares),
]