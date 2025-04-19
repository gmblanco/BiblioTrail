from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalogo.views import cargar_bibliotecas
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta, time
from reservas.models import ReservaEspacio
import httpx

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
                url = f"http://localhost:8000/espacios/api/disponibilidad/?espacio_id={espacio['id']}&biblioteca={biblioteca}&fecha={fecha}"
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

    return render(request, "espacios/disponibilidad.html", {
        "bibliotecas": bibliotecas,
        "biblioteca": biblioteca,
        "fecha": fecha,
        "horas": horas,
        "espacios": espacios
    })
