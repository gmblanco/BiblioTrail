from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import uuid

class Genero(models.Model):
    #Modelo para genero literiario (Ej: Literatura clásica, Fantasía...)

    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del género literario. (Ej: Fantasía, Terror...)")

    def __str__(self): 
        return self.nombre #devuelve el nombre del genero
    
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

class Idioma(models.Model):
    nombre = models.CharField(max_length=200, help_text="Ingrese el idioma (Ej:Inglés, Español, Italiano...)")

    def __str__(self): 
        return self.nombre #devuelve el nombre de la lengua

    class Meta:
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"

class Libro(models.Model):
    titulo = models.CharField(max_length=250)
    resumen = models.TextField(max_length=2000, help_text="Ingrese un breve resumen del libro")
    isbn = models.CharField('ISBN', max_length=13, help_text="Ingrese el ISBN del libro")
    editorial = models.CharField(max_length=200, help_text="Ingrese la editorial del libro")
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True, help_text="Seleccione el autor del libro")
    genero = models.ManyToManyField(Genero, help_text="Escoja un género para este libro")
    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True, help_text="Seleccione el idioma del libro")
    portada = models.ImageField(
        upload_to='portadas/',
        null=True,
        blank=True,
        help_text="Suba una imagen de portada para el libro",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('detalles-libro', args=[str(self.id)])

    def mostrar_generos(self):
        return ', '.join([genero.nombre for genero in self.genero.all()])
    mostrar_generos.short_description = 'Géneros'

    def mostrar_autor(self):
        if self.autor:
            return f"{self.autor.apellidos}, {self.autor.nombre}"
        return "Sin autor"
    mostrar_autor.short_description = 'Autor'

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"

class EjemplarLibro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este ejemplar")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)

    ESTADO_EJEMPLAR = (
        ('m', 'Mantenimiento'),
        ('p', 'Bajo prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_EJEMPLAR, blank=True, default='d', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["id"]
        verbose_name = "Ejemplar de libro"
        verbose_name_plural = "Ejemplares de libros"

    def __str__(self):
        return '%s (%s)' % (self.id, self.libro.titulo if self.libro else "Sin libro asociado")
    
    def esta_prestado(self):
        """Verifica si este ejemplar está actualmente prestado."""
        return self.estado == 'p'
    
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_defuncion = models.DateField(null=True, blank=True)
    biografia = models.TextField(max_length=2000, help_text="Ingrese una breve biografia del autor")

    def get_absolute_url(self):
        return reverse('detalles-autor', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.apellidos, self.nombre)
    class Meta:
        verbose_name = "Autor"  # Nombre singular
        verbose_name_plural = "Autores"  # Nombre en plural

class Prestamo(models.Model):
    #usuario = models.ForeignKey('autenticacion.PerfilUsuario', on_delete=models.CASCADE, help_text="Seleccione el usuario asociado a este préstamo")
    ejemplar = models.ForeignKey(EjemplarLibro, on_delete=models.CASCADE, help_text="Seleccione el ejemplar que se desea tomar a préstamo")
    fecha_prestamo = models.DateField(default=timezone.now)  # Fecha predeterminada a la fecha y hora actuales
    fecha_devolucion = models.DateField(null=True, blank=True, help_text="Fecha en que el libro fue devuelto")

    ESTADO_PRESTAMO = (
        ('a', 'Activo'),
        ('c', 'Completado'),
        ('r', 'Retrasado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_PRESTAMO, blank=True, default='a', help_text='Estado del préstamo')

    DIAS_PRESTAMO = 15  # Número de días predeterminado para devolver el libro

    class Meta:
        ordering = ["-fecha_prestamo"]
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"

    def __str__(self):
        return f'{self.ejemplar.libro.titulo} - ({self.estado})' #{self.usuario.username}

    def devolver(self):
        """Registra la devolución del libro y cambia el estado del ejemplar."""
        if self.fecha_devolucion is None: # Verificamos que no haya sido devuelto antes
            self.fecha_devolucion = timezone.now().date() # Establecemos la fecha de devolución
            self.estado = 'c'  # Marcamos el préstamo como completado
            self.ejemplar.estado = 'd'  # El ejemplar vuelve a estar disponible
            self.ejemplar.save() # Guardamos los cambios en el ejemplar
            self.save() # Guardamos los cambios en el préstamo

    @property
    def fecha_limite(self):
        """Calcula la fecha en la que el usuario debe devolver el libro (15 días después del préstamo)."""
        return self.fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)


    def actualizar_estado(self):
        """Actualiza el estado del préstamo dependiendo de la fecha de devolución y vencimiento."""
        if self.fecha_devolucion:  # Si ya fue devuelto
            self.estado = 'c'  # Completado
        elif timezone.now().date() > self.fecha_limite:  # Si pasó la fecha de vencimiento
            self.estado = 'r'  # Retrasado
        else:
            self.estado = 'a'  # Activo si aún está dentro del plazo

    @property
    def esta_vencido(self):
        """Verifica si el préstamo está vencido (sin devolver y con fecha de devolución pasada)."""
        return self.fecha_devolucion is None and self.estado == 'a' and self.fecha_prestamo < timezone.now().date()
    
    def save(self, *args, **kwargs):
        if self.fecha_devolucion:  # Si se ha devuelto el libro
            self.estado = 'c'  # Se marca como "Completado"
            self.ejemplar.estado = 'd'  # El ejemplar pasa a "Disponible"
            self.ejemplar.save()  # Guardamos el cambio en el ejemplar
        elif not self.pk:  # Si es un nuevo préstamo
            if self.ejemplar.estado == 'd':  # Solo si el ejemplar está disponible
                self.ejemplar.estado = 'p'  # Cambiamos a "Bajo préstamo"
                self.ejemplar.save()  # Guardamos el ejemplar con el nuevo estado

        self.actualizar_estado()  # Actualizamos el estado del préstamo
        super().save(*args, **kwargs)  # Llamamos al save() del modelo base
