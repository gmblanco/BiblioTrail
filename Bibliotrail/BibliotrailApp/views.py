import os
import requests
from django.shortcuts import render
from django.conf import settings
from itertools import islice

def agrupar_en_grupos(lista, n):
    """Genera sublistas de tamaño n"""
    return [lista[i:i + n] for i in range(0, len(lista), n)]

def inicio(request):
    libros = []

    ruta_bibliotecas = os.path.join(settings.BASE_DIR, 'bibliotecas.txt')

    try:
        with open(ruta_bibliotecas, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                nombre, host = linea.strip().split(',')
                url = f'http://{host}/api/libros/?limit=10'
                try:
                    respuesta = requests.get(url, timeout=3)
                    if respuesta.status_code == 200:
                        data = respuesta.json()
                        for libro in data:
                            libro['origen'] = host
                            libros.append(libro)
                except Exception as e:
                    print(f"Error accediendo a {nombre}: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo bibliotecas.txt")

    libros_agrupados = agrupar_en_grupos(libros[:30], 5)

    return render(request, 'BibliotrailApp/inicio.html', {
        'grupos_libros': libros_agrupados
    })



def eventos(request):
    
    return render(request, "BibliotrailApp/eventos.html")

