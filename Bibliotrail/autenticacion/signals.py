from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario

# Crear el perfil de usuario cuando se crea un nuevo usuario
@receiver(post_save, sender=User)
def crearPerfil(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            nombre=instance.first_name,
            apellido=instance.last_name,
        )

# Actualizar el usuario cuando el perfil es actualizado
@receiver(post_save, sender=PerfilUsuario)
def actualizarUsuario(sender, instance, created, **kwargs):
    if not created: 
        user = instance.user
        if user.first_name != instance.nombre or user.email != instance.email:
            user.first_name = instance.nombre
            user.email = instance.email
            user.save()

@receiver(post_delete, sender=PerfilUsuario)
def eliminarUsuario(sender, instance, **kwargs):
    user = getattr(instance, 'user', None)
    if user:  # Verifica si el usuario existe
        try:
            user.delete()  # Elimina el usuario
        except User.DoesNotExist:
            pass  # El usuario ya no existe, no hay nada que eliminar

