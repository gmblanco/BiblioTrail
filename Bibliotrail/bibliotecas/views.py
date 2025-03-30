from django.shortcuts import render

def bibliotecas(request):  
    import os
    import requests
    from django.conf import settings

    ruta_archivo = os.path.join(settings.BASE_DIR, 'bibliotecas.txt')
    print("Ruta del archivo:", ruta_archivo)

    bibliotecas = []

    try:
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                print(f"Línea: {linea}")
                nombre, host = linea.strip().split(',')
                url = f"http://{host}/api/info/"
                print(f"Consultando {url}")

                try:
                    response = requests.get(url, timeout=3)
                    print(f"→ Respuesta: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        data["nombre_sistema"] = nombre
                        bibliotecas.append(data)
                except Exception as e:
                    print(f"Error al consultar {host}: {e}")
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")

    return render(request, 'bibliotecas/bibliotecas.html', {'bibliotecas': bibliotecas})