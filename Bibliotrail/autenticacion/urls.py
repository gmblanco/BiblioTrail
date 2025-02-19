from django.urls import path
from .views import VistaRegistro, cerrar_sesion, iniciar_sesion, perfil, editarPerfil

urlpatterns = [
    path('', VistaRegistro.as_view(),name="registro"),
    path('cerrar_sesion/',cerrar_sesion,name="cerrar_sesion"),
    path('iniciar_sesion/',iniciar_sesion,name="iniciar_sesion"),
    path('perfil/', perfil,name="perfil"),
    path('editar_perfil/', editarPerfil,name="editar_perfil"),
]