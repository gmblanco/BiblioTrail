from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    nombre = models.CharField(max_length=200, blank=True, null=True)
    apellido = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    dni = models.CharField(max_length=9, unique=True, blank=True, null=True, help_text="Ingrese su DNI")
    sexo = models.CharField(max_length=6, choices=[('M', 'Hombre'), ('F', 'Mujer')], blank=True, null=True)
    direccion = models.TextField(max_length=250, blank=True, null=True, help_text="Ingrese la dirección de su domicilio")
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    ciudad = models.CharField(max_length=40, blank=True, null=True)
    provincia = models.CharField(max_length=40, blank=True, null=True)
    avatar = models.ImageField(null=True,blank=True , default="avatar.svg")
    bio = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ['created']
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

"""# Crear y Guardar perfil automaticamente:
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'perfil'):
        PerfilUsuario.objects.create(user=instance)"""

"""@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()"""