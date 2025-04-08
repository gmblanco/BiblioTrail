from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from catalogo.views import cargar_bibliotecas
from .models import *
import httpx
from dateutil.parser import parse 
from django.http import JsonResponse
from catalogo.views import cargar_bibliotecas
from django.views.decorators.http import require_GET

def eventos(request):
    bibliotecas = cargar_bibliotecas()
    biblioteca = request.GET.get("biblioteca", "")
    eventos = []
    eventos_inscritos = []
    if request.user.is_authenticated:
        eventos_inscritos = InscripcionEvento.objects.filter(usuario=request.user.perfil)
        eventos_inscritos = {(i.evento_id, i.biblioteca_origen) for i in eventos_inscritos}

    if biblioteca and biblioteca in bibliotecas:
        base_url = bibliotecas[biblioteca]
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"

        try:
            r = httpx.get(f"{base_url}/api/eventos/", timeout=10.0)
            if r.status_code == 200:
                eventos = r.json()
                for evento in eventos:
                    evento["biblioteca_id"] = biblioteca
                    evento["plazas_disponibles"] = evento["plazas_totales"] - evento["plazas_ocupadas"]
                    evento["ya_inscrito"] = (evento["id"], biblioteca) in eventos_inscritos

                    try:
                        evento["fecha_inicio"] = parse(evento["fecha_inicio"])
                        evento["fecha_fin"] = parse(evento["fecha_fin"]) if evento.get("fecha_fin") else None
                    except Exception as e:
                        print("Error al convertir fechas:", e)
                        evento["fecha_inicio"] = None
                        evento["fecha_fin"] = None

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
        return redirect("Eventos")

    try:
        r = httpx.get(f"{base_url}/api/eventos/{evento_id}/", timeout=10.0)
        if r.status_code == 200:
            datos_evento = r.json()
            inscripcion, creada = InscripcionEvento.objects.get_or_create(
                usuario=request.user.perfil,
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

    return redirect("Eventos")



@require_GET
@login_required
def eventos_calendario_json(request):
    biblioteca = request.GET.get("biblioteca", "")
    bibliotecas = cargar_bibliotecas()
    eventos_fc = []

    if biblioteca and biblioteca in bibliotecas:
        base_url = bibliotecas[biblioteca]
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"

        try:
            r = httpx.get(f"{base_url}/api/eventos/", timeout=10.0)
            if r.status_code == 200:
                eventos = r.json()

                for evento in eventos:
                    eventos_fc.append({
                        "id": evento["id"],
                        "title": evento["titulo"],
                        "start": evento["fecha_inicio"],
                        "end": evento["fecha_fin"],
                        "extendedProps": {
                            "lugar": evento["lugar"],
                            "biblioteca": biblioteca,
                            "plazas_disponibles": evento["plazas_totales"] - evento["plazas_ocupadas"]
                        }
                    })
        except httpx.RequestError:
            pass  # puedes loggear o devolver error si quieres

    return JsonResponse(eventos_fc, safe=False)

@login_required
def calendario(request):
    bibliotecas = cargar_bibliotecas()
    biblioteca = request.GET.get("biblioteca", "")

    if not biblioteca and bibliotecas:
        biblioteca = list(bibliotecas.keys())[0]

    return render(request, "eventos/calendario.html", {
        "bibliotecas": bibliotecas,
        "biblioteca": biblioteca
    })
