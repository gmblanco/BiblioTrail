from django.db import models
from django.utils import timezone
from autenticacion.models import PerfilUsuario
from datetime import timedelta
from catalogo.views import cargar_bibliotecas
import httpx

# Create your models here.
class InscripcionEvento(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    evento_id = models.PositiveIntegerField()
    titulo_evento = models.CharField(max_length=200)
    biblioteca_origen = models.CharField(max_length=100)
    fecha_inscripcion = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('usuario', 'evento_id', 'biblioteca_origen')
        verbose_name = "Inscripción a evento"
        verbose_name_plural = "Inscripciones a eventos"

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo_evento} [{self.biblioteca_origen}]"

    def save(self, *args, **kwargs):
        es_nueva = self._state.adding
        super().save(*args, **kwargs)

        if es_nueva:
            base_url = None

            if self.biblioteca_origen.startswith("http"):
                base_url = self.biblioteca_origen.rstrip('/')
            else:
                bibliotecas = cargar_bibliotecas()
                base_url = bibliotecas.get(self.biblioteca_origen)

            if base_url:
                url = f"{base_url}/api/eventos/{self.evento_id}/inscripciones/"
                payload = {
                    "email": self.usuario.email,
                    "nombre": self.usuario.get_nombre_completo(),
                }

                try:
                    response = httpx.post(url, json=payload, timeout=10.0)
                    if response.status_code in [200, 201]:
                        print(f"Usuario inscrito en evento {self.evento_id}")
                    else:
                        print(f"Error al inscribirse: {response.status_code} - {response.text}")
                except httpx.RequestError as e:
                    print(f"Error de conexión con la biblioteca: {e}")
            else:
                print(f"No se encontró la URL para la biblioteca '{self.biblioteca_origen}'")