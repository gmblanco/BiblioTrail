from django.contrib import admin
from .models import *

@admin.register(ReservaEspacio)
class ReservaEspacioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo_espacio', 'biblioteca_origen', 'fecha', 'hora_inicio', 'hora_fin')
    list_filter = ('biblioteca_origen', 'fecha')
    search_fields = ('titulo_espacio', 'usuario__user__username')  
