from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import *
import requests
import httpx
import urllib.parse


def catalogo(request):
    #sesiones
    num_visitas = request.session.get('num_visitas',0)
    num_visitas += 1
    request.session['num_visitas'] = num_visitas

    contexto = {
        'num_visitas':num_visitas,
    }

    return render(request, "catalogo/catalogo.html",contexto)

def cargar_bibliotecas():
    bibliotecas = {}
    with open("bibliotecas.txt", "r") as f:
        for linea in f:
            if ',' in linea:
                nombre, url = linea.strip().split(',', 1)
                bibliotecas[nombre.strip()] = url.strip()
    return bibliotecas

def buscar_libros(request):
    query = request.GET.get('q', '')
    biblioteca = request.GET.get('biblioteca', '')
    genero = request.GET.get('genero', '')

    bibliotecas = cargar_bibliotecas()
    resultados = []

    if biblioteca and biblioteca in bibliotecas:
        urls = [f"http://{bibliotecas[biblioteca]}/api/libros/"]
    else:
        urls = [f"http://{url}/api/libros/" for url in bibliotecas.values()]
    
    for url in urls:
        try:
            params = {}
            if query:
                params['search'] = query
            if genero:
                params['genero'] = genero

            # Imprime la URL real codificada
            url_completa = f"{url}?{urllib.parse.urlencode(params)}"
            print("URL completa:", url_completa)

            response = httpx.get(url, params=params, timeout=10.0)
            
            if response.status_code == 200:
                datos = response.json()
                if isinstance(datos, dict) and 'results' in datos:
                    libros = datos['results']
                elif isinstance(datos, list):
                    libros = datos
                else:
                    libros = []

                for libro in libros:
                    libro['biblioteca_url'] = url.split('/api')[0]
                    resultados.append(libro)

        except httpx.RequestError:
            pass
    return render(request, 'catalogo/catalogo.html', {
        'resultados': resultados,
        'query': query,
        'biblioteca': biblioteca,
        'genero': genero,
        'bibliotecas': bibliotecas,  # Pasamos todo el diccionario
    })

from django.shortcuts import render
import httpx

def detalles_libro(request):
    libro_id = request.GET.get("libro_id")
    biblioteca_url = request.GET.get("biblioteca_url")

    if not libro_id or not biblioteca_url:
        return render(request, "catalogo/error.html")

    url = f"{biblioteca_url}/api/libros/{libro_id}/"
    print("URL que voy a pedir:", url)

    try:
        response = httpx.get(url, timeout=10.0)

        print("Código de estado:", response.status_code)
        print("Contenido de la respuesta:", response.text)

        if response.status_code == 200:
            data = response.json()
            print("JSON decodificado:", data)

            libro = data.get("libro")
            ejemplares_todos = data.get("ejemplares", [])
            ejemplares = [e for e in ejemplares_todos if e.get("estado") == "d"]

            if libro is None:
                print("La clave 'libro' no está en el JSON")
                return render(request, "catalogo/error.html")

            context = {
                "libro": libro,
                "ejemplares": ejemplares,
                "biblioteca_url": biblioteca_url
            }

            return render(request, "catalogo/detalles_libro.html", context)

        else:
            return render(request, "catalogo/error.html")

    except httpx.RequestError as e:
        print("Error de conexión con la API:", e)
        return render(request, "catalogo/error.html")

def detalles_autor(request):
    autor_id = request.GET.get("autor_id")
    biblioteca_url = request.GET.get("biblioteca_url")

    if not autor_id or not biblioteca_url:
        return render(request, "catalogo/error.html")

    url = f"{biblioteca_url}/api/autores/{autor_id}/"
    print("URL que voy a pedir:", url)

    try:
        response = httpx.get(url, timeout=10.0)

        print("Código de estado:", response.status_code)
        print("Contenido de la respuesta:", response.text)

        if response.status_code == 200:
            data = response.json()
            print("JSON decodificado:", data)

            autor = data.get("autor")

            if autor is None:
                print("La clave 'autor' no está en el JSON")
                return render(request, "catalogo/error.html")

            context = {
                "autor": autor,
                "biblioteca_url": biblioteca_url
            }

            return render(request, "catalogo/detalles_autor.html", context)

        else:
            return render(request, "catalogo/error.html")

    except httpx.RequestError as e:
        print("Error de conexión con la API:", e)
        return render(request, "catalogo/error.html")

@login_required
def prestar_ejemplar(request, ejemplar_id):
    if request.method == "POST":
        usuario = request.user.perfil 

        api_base = "http://127.0.0.1:8001"
        ejemplar_url = f"{api_base}/api/ejemplares/{ejemplar_id}/"

        # Paso 1: Obtener datos del ejemplar
        response = requests.get(ejemplar_url)

        if response.status_code == 200:
            ejemplar_data = response.json()
            titulo_libro = ejemplar_data["libro"]["titulo"]

            # Paso 2: Marcar como prestado en la biblioteca externa
            patch_response = requests.patch(ejemplar_url, json={"estado": "p"})

            if patch_response.status_code in [200, 202]:
                # Paso 3: Crear el préstamo local
                PrestamoUsuario.objects.create(
                    usuario=usuario,
                    titulo_libro=titulo_libro,
                    biblioteca_origen="biblioteca1",
                    ejemplar_id=str(ejemplar_id),
                    fecha_prestamo=timezone.now(),
                    estado='a',
                )
                messages.success(request, f"Has prestado «{titulo_libro}».")
            else:
                messages.error(request, "Error al marcar el ejemplar como prestado.")
        else:
            messages.error(request, "No se pudo obtener el ejemplar.")

        return redirect("Catalogo")
