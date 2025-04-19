from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalogo.models import PrestamoUsuario
from eventos.models import InscripcionEvento
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from catalogo.views import cargar_bibliotecas
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta, time
from .models import ReservaEspacio
import httpx
from django.utils.safestring import mark_safe
import json
# Recupera detalles del libro desde la API de la biblioteca correspondiente
def obtener_datos_libro(prestamo):
    base_url = prestamo.biblioteca_origen
    if not base_url.startswith("http"):
        from catalogo.models import cargar_bibliotecas
        bibliotecas = cargar_bibliotecas()
        base_url = bibliotecas.get(prestamo.biblioteca_origen)

    if not base_url:
        return {}

    try:
        # Petición a la API de ejemplares
        url = f"{base_url}/api/ejemplares/{prestamo.ejemplar_id}/"
        response = httpx.get(url, timeout=10.0)
        if response.status_code == 200:
            ejemplar = response.json()
            libro = ejemplar.get("libro", {})
            portada = libro.get("portada")
            if portada and portada.startswith("/media/"):
                portada = f"{base_url.rstrip('/')}{portada}"

            return {
                "id": libro.get("id"),
                "titulo": libro.get("titulo"),
                "portada": portada,
                "autor": f"{libro.get('autor', {}).get('nombre', '')} {libro.get('autor', {}).get('apellidos', '')}",
                "editorial": libro.get("editorial"),
                "resumen": libro.get("resumen"),
                "isbn": libro.get("isbn"),
                "biblioteca_url": base_url,
            }
    except Exception as e:
        print(f"Error al consultar API del libro: {e}")

    return {}

# Vista general de "Mis reservas" (placeholder)
def reservas(request):
    return render(request, "reservas/reservas.html")

# Vista de préstamos personales
@login_required
def mis_prestamos(request):
    usuario = request.user.perfil
    prestamos_qs = PrestamoUsuario.objects.filter(usuario=usuario, estado__in=['a', 'r'])

    prestamos_activos = []
    for prestamo in prestamos_qs:
        libro = obtener_datos_libro(prestamo)
        if libro:
            prestamos_activos.append({
                "id": prestamo.id,
                "titulo_libro": libro.get("titulo", prestamo.titulo_libro),
                "fecha_prestamo": prestamo.fecha_prestamo,
                "fecha_limite": prestamo.fecha_limite,
                "estado": prestamo.estado,
                "portada": libro.get("portada"),
                "autor": libro.get("autor"),
                "editorial": libro.get("editorial"),
                "resumen": libro.get("resumen"),
                "isbn": libro.get("isbn"),
                "libro_id": libro.get("id"),
                "biblioteca_url": libro.get("biblioteca_url"),
            })

    prestamos_devueltos = PrestamoUsuario.objects.filter(usuario=usuario, estado='d')

    return render(request, "reservas/mis_prestamos.html", {
        "prestamos_activos": prestamos_activos,
        "prestamos_devueltos": prestamos_devueltos,
    })

@login_required
def mis_inscripciones(request):
    inscripciones = InscripcionEvento.objects.filter(usuario=request.user.perfil).order_by("-fecha_inscripcion")
    return render(request, "reservas/mis_inscripciones.html", {
        "inscripciones": inscripciones
    })


@login_required
def cancelar_inscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(InscripcionEvento, id=inscripcion_id, usuario=request.user.perfil)
    
    # Guardar datos antes de eliminar
    evento_id = inscripcion.evento_id
    biblioteca = inscripcion.biblioteca_origen

    # Eliminar inscripción
    inscripcion.delete()
    messages.success(request, "Te has dado de baja del evento.")

    # Disminuir plazas ocupadas en la biblioteca externa
    bibliotecas = cargar_bibliotecas()
    base_url = bibliotecas.get(biblioteca)
    if base_url and not base_url.startswith("http"):
        base_url = f"http://{base_url}"
    
    try:
        patch = httpx.patch(f"{base_url}/api/eventos/{evento_id}/", json={"disminuir_ocupadas": True}, timeout=10.0)
        print("PATCH baja:", patch.status_code, patch.text)
    except httpx.RequestError:
        print("Error de conexión al intentar liberar plaza")

    return redirect('mis_inscripciones')

"""class DisponibilidadEspacioAPIView(APIView):
    def get(self, request):
        espacio_id = request.query_params.get("espacio_id")
        biblioteca = request.query_params.get("biblioteca")
        fecha = request.query_params.get("fecha")

        if not espacio_id or not biblioteca or not fecha:
            return Response({"error": "Faltan parámetros"}, status=400)

        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}, status=400)

        bloques = []
        hora = time(8, 0)
        fin = time(21, 0)
        delta = timedelta(minutes=30)

        while hora < fin:
            siguiente = (datetime.combine(fecha, hora) + delta).time()
            reservado = ReservaEspacio.objects.filter(
                espacio_id_remoto=espacio_id,
                biblioteca_origen=biblioteca,
                fecha=fecha,
                hora_inicio__lt=siguiente,
                hora_fin__gt=hora
            ).exists()
            bloques.append({
                "start": f"{fecha}T{hora.strftime('%H:%M')}",
                "end": f"{fecha}T{siguiente.strftime('%H:%M')}",
                "title": "No disponible" if reservado else "Disponible",
                "backgroundColor": "#d9534f" if reservado else "#5cb85c"
            })
            hora = siguiente

        return Response(bloques)

@login_required
def disponibilidad_matriz(request):
    bibliotecas = cargar_bibliotecas()
    biblioteca = request.GET.get("biblioteca", "")
    fecha_str = request.GET.get("fecha")

    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha = datetime.today().date()
    else:
        fecha = datetime.today().date()


    if not biblioteca and bibliotecas:
        biblioteca = list(bibliotecas.keys())[0] #si no se ha seleccionado biblioteca cojo la primera de la lista

    base_urls = bibliotecas
    base_url = base_urls.get(biblioteca)
    if base_url and not base_url.startswith("http"):
        base_url = f"http://{base_url}"

    # 1. Definir las horas disponibles
    hora_actual = time(8, 0)
    fin = time(21, 0)
    delta = timedelta(minutes=30)
    horas = []

    while hora_actual < fin:
        horas.append(hora_actual.strftime("%H:%M"))
        hora_actual = (datetime.combine(fecha, hora_actual) + delta).time()

    espacios = []

    # 2. Obtener los espacios
    try:
        r = httpx.get(f"{base_url}/api/espacios/", timeout=10.0)
        if r.status_code == 200:
            lista_espacios = r.json()

            for espacio in lista_espacios:
                url = f"http://localhost:8000/reservas/api/disponibilidad/?espacio_id={espacio['id']}&biblioteca={biblioteca}&fecha={fecha}"
                try:
                    r_bloques = httpx.get(url, timeout=10.0)
                    bloques_api = r_bloques.json() if r_bloques.status_code == 200 else []
                except:
                    bloques_api = []

                bloques = []
                for hora_str in horas:
                    bloque_actual = next((b for b in bloques_api if b["start"].endswith(hora_str)), None)
                    disponible = bloque_actual and bloque_actual["title"] == "Disponible"
                    siguiente = (datetime.strptime(hora_str, "%H:%M") + delta).strftime("%H:%M")
                    bloques.append({
                        "hora_inicio": hora_str,
                        "hora_fin": siguiente,
                        "disponible": disponible
                    })

                espacios.append({
                    "id": espacio["id"],
                    "nombre": espacio["nombre"],
                    "bloques": bloques
                })


    except httpx.RequestError as e:
        print("Error al cargar espacios:", e)

    return render(request, "reservas/disponibilidad.html", {
        "bibliotecas": bibliotecas,
        "biblioteca": biblioteca,
        "fecha": fecha,
        "horas": horas,
        "espacios": espacios
    })"""


@csrf_exempt
@require_POST
@login_required
def crear_reserva_espacio(request):
    import json
    datos = json.loads(request.body)

    espacio_id = datos.get("espacio_id")
    titulo = datos.get("titulo")
    biblioteca = datos.get("biblioteca")
    fecha = datos.get("fecha")
    hora_inicio = datos.get("hora_inicio")
    hora_fin = datos.get("hora_fin")

    if not all([espacio_id, titulo, biblioteca, fecha, hora_inicio, hora_fin]):
        return JsonResponse({"error": "Faltan datos"}, status=400)

    try:
        ReservaEspacio.objects.create(
            usuario=request.user.perfil,
            espacio_id_remoto=espacio_id,
            titulo_espacio=titulo,
            biblioteca_origen=biblioteca,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def mis_espacios(request):
    reservas = ReservaEspacio.objects.filter(usuario=request.user.perfil).order_by("-fecha", "-hora_inicio")
    return render(request, "reservas/mis_espacios.html", {
        "reservas": reservas
    })
@login_required
def cancelar_reserva_espacio(request, reserva_id):
    reserva = get_object_or_404(ReservaEspacio, id=reserva_id, usuario=request.user.perfil)
    reserva.delete()
    messages.success(request, "Has cancelado la reserva correctamente.")
    return redirect("mis_espacios")
