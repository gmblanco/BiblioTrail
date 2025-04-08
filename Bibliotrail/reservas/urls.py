from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas,name="Reservas"),
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('cancelar-inscripcion/<int:inscripcion_id>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
]