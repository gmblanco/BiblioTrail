from django.contrib import admin
from django.db import models 
from .models import Autor, Genero, Libro, Idioma, EjemplarLibro, PerfilUsuario, Prestamo
from django.utils.html import format_html

admin.site.register(Genero)
admin.site.register(Idioma)

class EjemplarLibroInline(admin.TabularInline):
    model = EjemplarLibro

class LibroInline(admin.StackedInline):
    model = Libro.autor.through
    extra = 1

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellidos', 'nombre', 'fecha_nacimiento', 'fecha_defuncion')
    fields = ['apellidos', 'nombre', ('fecha_nacimiento', 'fecha_defuncion')]
    inlines = [LibroInline]

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mostrar_autores', 'mostrar_generos', 'idioma')
    inlines = [EjemplarLibroInline]

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejemplar', 'aviso_estado' ,'fecha_prestamo', 'fecha_devolucion','fecha_limite')
    list_filter = ('estado', 'fecha_prestamo', 'fecha_devolucion')
    search_fields = ('usuario__user__username', 'usuario__dni', 'ejemplar__libro__titulo')
    readonly_fields = ('estado',)
    fieldsets = (
        (None, {
            'fields': ('usuario', 'ejemplar', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_prestamo', 'fecha_devolucion')
        }),
    )   

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ejemplar":
            # Si estamos editando un préstamo, incluimos el ejemplar ya seleccionado
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                prestamo_actual = Prestamo.objects.get(id=obj_id)
                kwargs["queryset"] = EjemplarLibro.objects.filter(models.Q(estado='d') | models.Q(id=prestamo_actual.ejemplar.id))
            else:
                kwargs["queryset"] = EjemplarLibro.objects.filter(estado='d')  # Solo disponibles al crear un préstamo
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    def aviso_estado(self, obj):
        if obj.estado == 'r':  # Si el estado es "Retrasado"
            return format_html('<span style="color: red;">{}</span>', obj.get_estado_display())
        elif obj.estado == 'a':
            return format_html('<span style="color: green;">{}</span>', obj.get_estado_display())
        return obj.get_estado_display()  # Mostrar el estado normal
    aviso_estado.short_description = 'Estado'

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('dni', 'direccion','codigo_postal','ciudad','sexo', 'user')  # Campos para mostrar
    search_fields = ['dni', 'user__username','sexo', 'user__email']
    fieldsets = (
        (None, {
            'fields': ('user', 'dni','sexo', 'direccion')
        }),
    )
@admin.register(EjemplarLibro)
class EjemplarLibroAdmin(admin.ModelAdmin):
    list_display = ('libro', 'estado', 'id')
    list_filter = ('estado',)
    fieldsets = (
        (None, {
            'fields': ('libro', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('estado',)
        }),
    )