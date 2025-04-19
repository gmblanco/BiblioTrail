from django.db import models
from autenticacion.models import PerfilUsuario

class ReservaEspacio(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    espacio_id_remoto = models.PositiveIntegerField()
    titulo_espacio = models.CharField(max_length=200)
    biblioteca_origen = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('espacio_id_remoto', 'biblioteca_origen', 'fecha', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.usuario} - {self.titulo_espacio} ({self.fecha} {self.hora_inicio}-{self.hora_fin})"
