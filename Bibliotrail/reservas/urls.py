from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.reservas,name="Reservas"),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('cancelar-inscripcion/<int:inscripcion_id>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    #path('api/disponibilidad/', DisponibilidadEspacioAPIView.as_view(), name='disponibilidad-espacio'),
    #path("calendario_espacios/", disponibilidad_matriz, name="calendario_espacios"),
    path("api/reservar/", views.crear_reserva_espacio, name="crear_reserva_espacio"),
    path("mis-espacios/", views.mis_espacios, name="mis_espacios"),
    path("cancelar-reserva/<int:reserva_id>/", views.cancelar_reserva_espacio, name="cancelar_reserva_espacio"),
]