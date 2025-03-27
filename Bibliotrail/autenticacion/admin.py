from django.contrib import admin
from django.db import models 
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user','email','nombre','apellido','username' ,'direccion','codigo_postal','ciudad','provincia','sexo','dni', 'avatar', 'bio' )  # Campos para mostrar
    search_fields = [ 'user__username','sexo', 'user__email']
    fieldsets = (
        (None, {
            'fields': ('user','email','nombre','apellido','username' ,'direccion','codigo_postal','ciudad','provincia','sexo','dni', 'avatar', 'bio')
        }),
    )