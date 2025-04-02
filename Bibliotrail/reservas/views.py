from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalogo.models import PrestamoUsuario
import httpx

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
