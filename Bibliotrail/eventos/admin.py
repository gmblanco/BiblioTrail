from django.contrib import admin
from .models import *

@admin.register(InscripcionEvento)
class InscripcionEventoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'titulo_evento',
        'biblioteca_origen',
        'fecha_inscripcion',
    )
    list_filter = ('biblioteca_origen', 'fecha_inscripcion')
    search_fields = ('usuario__user__username', 'titulo_evento', 'biblioteca_origen')
    ordering = ('-fecha_inscripcion',)
