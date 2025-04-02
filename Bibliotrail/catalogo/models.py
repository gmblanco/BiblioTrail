from django.db import models
from django.utils import timezone
from autenticacion.models import PerfilUsuario
import httpx

def cargar_bibliotecas():
        bibliotecas = {}
        try:
            with open("bibliotecas.txt", "r") as f:
                for linea in f:
                    if ',' in linea:
                        nombre, url = linea.strip().split(',', 1)
                        bibliotecas[nombre.strip()] = f"http://{url.strip()}"
        except FileNotFoundError:
            print("⚠ No se encontró el archivo bibliotecas.txt")
        return bibliotecas

class PrestamoUsuario(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    titulo_libro = models.CharField(max_length=200)  # Título del libro prestado
    biblioteca_origen = models.CharField(max_length=100)  # Ej: "biblioteca1" o una URL base
    ejemplar_id = models.CharField(max_length=100)  # UUID o ID que recibo desde la API de la biblioteca
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)

    ESTADO = (
        ('a', 'Activo'),
        ('d', 'Devuelto'),
        ('r', 'Retrasado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO, default='a')

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name = "Préstamo de usuario"
        verbose_name_plural = "Préstamos de usuarios"

    def __str__(self):
        return f"{self.titulo_libro} - {self.usuario.username} ({self.get_estado_display()})"

    def marcar_como_devuelto(self):
        self.fecha_devolucion = timezone.now().date()
        self.estado = 'd'
        self.save()

    #actualizar el estado del ejemplar en las bbdd de las bibliotecas
    def save(self, *args, **kwargs):
        prestamo_anterior = None
        if self.pk:
            prestamo_anterior = PrestamoUsuario.objects.get(pk=self.pk)

        super().save(*args, **kwargs)

        if prestamo_anterior and prestamo_anterior.estado != self.estado:
            base_url = None

            # Si ya es una URL completa, úsala directamente
            if self.biblioteca_origen.startswith("http"):
                base_url = self.biblioteca_origen.rstrip('/')
            else:
                # Buscar la URL en bibliotecas.txt
                bibliotecas = cargar_bibliotecas()
                base_url = bibliotecas.get(self.biblioteca_origen)

            if base_url:
                url = f"{base_url}/api/ejemplares/{self.ejemplar_id}/"
                nuevo_estado_ejemplar = "d" if self.estado == "d" else "p"

                try:
                    response = httpx.patch(url, json={"estado": nuevo_estado_ejemplar}, timeout=10.0)
                    if response.status_code in [200, 202]:
                        print(f"✔ Estado del ejemplar actualizado a '{nuevo_estado_ejemplar}' por cambio a '{self.estado}'")
                    else:
                        print(f"Error al actualizar ejemplar: {response.status_code}")
                except httpx.RequestError as e:
                    print(f"Error al conectar con la biblioteca externa: {e}")
            else:
                print(f"⚠ No se encontró la URL base para: {self.biblioteca_origen}")
