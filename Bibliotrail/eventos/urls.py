from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.eventos, name="Eventos"),
    path('<str:biblioteca_id>/<int:evento_id>/inscribirse/', views.inscripcion_evento, name='inscripcion_evento'),
    path("calendario/eventos/", views.eventos_calendario_json, name="eventos_calendario_json"),
    path("calendario/", views.calendario, name="calendario"),
]