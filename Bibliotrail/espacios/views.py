import httpx, json
import asyncio
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalogo.views import cargar_bibliotecas
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta, time
from reservas.models import ReservaEspacio
from asgiref.sync import sync_to_async


def espacios(request):
    return render(request, "espacios/disponibilidad.html")

class DisponibilidadEspacioAPIView(APIView):
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
    capacidad_minima = int(request.GET.get("capacidad_minima", 0))

    # Procesar la fecha
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha = datetime.today().date()
    else:
        fecha = datetime.today().date()

    # Generar lista de horas
    hora_actual = time(8, 0)
    fin = time(21, 0)
    delta = timedelta(minutes=30)
    horas = []

    while hora_actual < fin:
        horas.append(hora_actual.strftime("%H:%M"))
        hora_actual = (datetime.combine(fecha, hora_actual) + delta).time()

    # Cargar espacios
    espacios = []
    if biblioteca == "todas":
        for clave, base_url in bibliotecas.items():
            if not base_url.startswith("http"):
                base_url = f"http://{base_url}"
            espacios += cargar_espacios(clave, base_url, fecha, horas, capacidad_minima)
    else:
        base_url = bibliotecas.get(biblioteca, "")
        if not base_url.startswith("http"):
            base_url = f"http://{base_url}"
        espacios += cargar_espacios(biblioteca, base_url, fecha, horas, capacidad_minima)

    return render(request, "espacios/disponibilidad.html", {
        "bibliotecas": bibliotecas,
        "biblioteca": biblioteca,
        "fecha": fecha,
        "horas": horas,
        "espacios": espacios
    })


def cargar_espacios(biblioteca_id, base_url, fecha, horas, capacidad_minima):
    espacios = []
    try:
        r = httpx.get(f"{base_url}/api/espacios/", timeout=10.0)
        r_dispo = httpx.get(
            f"http://localhost:8000/espacios/api/disponibilidad-general/?biblioteca={biblioteca_id}&fecha={fecha}",
            timeout=10.0
        )

        if r.status_code == 200:
            lista_espacios = r.json()
            reservas_por_espacio = r_dispo.json() if r_dispo.status_code == 200 else {}

            for espacio in lista_espacios:
                if espacio.get("capacidad", 0) < capacidad_minima:
                    continue

                espacio_id = str(espacio["id"])
                reservas = reservas_por_espacio.get(espacio_id, [])
                bloques = []

                for hora_str in horas:
                    inicio = datetime.strptime(hora_str, "%H:%M").time()
                    fin_bloque = (datetime.combine(fecha, inicio) + timedelta(minutes=30)).time()

                    ocupado = any(
                        datetime.strptime(r[0], "%H:%M:%S").time() < fin_bloque and
                        datetime.strptime(r[1], "%H:%M:%S").time() > inicio
                        for r in reservas
                    )

                    bloques.append({
                        "hora_inicio": hora_str,
                        "hora_fin": fin_bloque.strftime("%H:%M"),
                        "disponible": not ocupado
                    })

                espacios.append({
                    "id": espacio["id"],
                    "nombre": espacio["nombre"],
                    "ubicacion": espacio.get("ubicacion", ""),
                    "capacidad": espacio.get("capacidad", ""),
                    "bloques": bloques,
                    "biblioteca": biblioteca_id  # para mostrar en la tabla
                })
    except httpx.RequestError as e:
        print(f"Error al consultar {biblioteca_id}: {e}")
    return espacios

from django.http import JsonResponse

class DisponibilidadGeneralAPIView(APIView):
    def get(self, request):
        biblioteca = request.query_params.get("biblioteca")
        fecha = request.query_params.get("fecha")

        if not biblioteca or not fecha:
            return Response({"error": "Faltan parámetros"}, status=400)

        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Fecha inválida"}, status=400)

        reservas = ReservaEspacio.objects.filter(
            biblioteca_origen=biblioteca,
            fecha=fecha
        ).values(
            "espacio_id_remoto", "hora_inicio", "hora_fin"
        )

        reservas_dict = {}
        for r in reservas:
            key = r["espacio_id_remoto"]
            if key not in reservas_dict:
                reservas_dict[key] = []
            reservas_dict[key].append((r["hora_inicio"], r["hora_fin"]))

        return JsonResponse(reservas_dict)
