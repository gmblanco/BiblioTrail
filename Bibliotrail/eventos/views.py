from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from catalogo.views import cargar_bibliotecas
from .models import *
import httpx

# Create your views here.
def eventos(request):
    bibliotecas = cargar_bibliotecas()
    biblioteca = request.GET.get("biblioteca", "")
    eventos = []

    print("Biblioteca seleccionada:", biblioteca)
    print("Bibliotecas disponibles:", bibliotecas)

    if biblioteca and biblioteca in bibliotecas:
        base_url = bibliotecas[biblioteca]
        # Asegurar que tenga http:// delante
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"

        try:
            r = httpx.get(f"{base_url}/api/eventos/", timeout=10.0)
            print("Código de respuesta:", r.status_code)
            print("Contenido recibido:", r.text)
            if r.status_code == 200:
                eventos = r.json()
                for evento in eventos:
                    evento["biblioteca_id"] = biblioteca
                    total = evento.get("plazas_totales", 0)
                    ocupadas = evento.get("plazas_ocupadas", 0)
                    evento["plazas_disponibles"] = total - ocupadas
                print("Eventos cargados:", eventos)
        except httpx.RequestError:
            messages.error(request, "No se pudo conectar con la biblioteca seleccionada.")

    return render(request, "eventos/eventos.html", {
        "bibliotecas": bibliotecas,
        "biblioteca": biblioteca,
        "eventos": eventos,
    })



@login_required
def inscripcion_evento(request, biblioteca_id, evento_id):
    bibliotecas = cargar_bibliotecas()
    base_url = bibliotecas.get(biblioteca_id)
    if base_url and not base_url.startswith("http"):
        base_url = f"http://{base_url}"

    if not base_url:
        messages.error(request, "Biblioteca no encontrada")
        return redirect("Catalogo")

    try:
        r = httpx.get(f"{base_url}/api/eventos/{evento_id}/", timeout=10.0)
        if r.status_code == 200:
            datos_evento = r.json()
            inscripcion, creada = InscripcionEvento.objects.get_or_create(
                usuario=request.user.perfilusuario,
                evento_id=evento_id,
                biblioteca_origen=biblioteca_id,
                defaults={"titulo_evento": datos_evento.get("titulo", "Sin título")}
            )
            if creada:
                messages.success(request, "Te has inscrito correctamente al evento.")
            else:
                messages.info(request, "Ya estabas inscrito en este evento.")
        else:
            messages.error(request, "No se pudo obtener información del evento.")
    except httpx.RequestError:
        messages.error(request, "Error de conexión con la biblioteca")

    return redirect("detalles_evento", biblioteca_id=biblioteca_id, evento_id=evento_id)