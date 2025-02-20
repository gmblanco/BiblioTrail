from django.urls import path
from .views import *

urlpatterns = [
    path('perfil/', perfil,name="perfil"),
    path('editar_perfil/', editarPerfil,name="editar_perfil"),
    path('register/', registerPage, name="register"),
    path('iniciar_sesion/',iniciar_sesion,name="iniciar_sesion"),
    path('cerrar_sesion/',cerrar_sesion,name="cerrar_sesion"),
]
