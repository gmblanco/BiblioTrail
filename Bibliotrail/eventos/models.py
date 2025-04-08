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
    
    def delete(self, *args, **kwargs):
        base_url = None

        if self.biblioteca_origen.startswith("http"):
            base_url = self.biblioteca_origen.rstrip('/')
        else:
            bibliotecas = cargar_bibliotecas()
            base_url = bibliotecas.get(self.biblioteca_origen)
            if base_url and not base_url.startswith("http"):
                base_url = f"http://{base_url}"

        if base_url:
            url_evento = f"{base_url}/api/eventos/{self.evento_id}/"
            try:
                patch = httpx.patch(url_evento, json={"decrementar_ocupadas": True}, timeout=10.0)
                print("🔁 PATCH baja:", patch.status_code, patch.text)
            except httpx.RequestError as e:
                print(f"❌ Error de conexión al liberar plaza: {e}")

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        es_nueva = self._state.adding
        super().save(*args, **kwargs)

        if es_nueva:
            # Obtener la URL base de la biblioteca
            if self.biblioteca_origen.startswith("http"):
                base_url = self.biblioteca_origen.rstrip('/')
            else:
                bibliotecas = cargar_bibliotecas()
                base_url = bibliotecas.get(self.biblioteca_origen)
                if base_url and not base_url.startswith("http"):
                    base_url = f"http://{base_url}"

            if base_url:
                # PATCH para incrementar plazas ocupadas
                url_evento = f"{base_url}/api/eventos/{self.evento_id}/"
                print(f"▶ Enviando PATCH a {url_evento} para incrementar plazas")

                try:
                    patch = httpx.patch(url_evento, json={"incrementar_ocupadas": True}, timeout=10.0)
                    print("🔁 PATCH respuesta:", patch.status_code, patch.text)

                    if patch.status_code in [200, 202]:
                        print("Plazas actualizadas correctamente")
                    else:
                        print(f"No se pudo actualizar plazas: {patch.status_code} - {patch.text}")

                except httpx.RequestError as e:
                    print(f"Error de conexión con la biblioteca: {e}")
            else:
                print(f"No se encontró la URL para la biblioteca '{self.biblioteca_origen}'")
