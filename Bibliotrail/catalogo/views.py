from django.shortcuts import render
import httpx
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="iniciar_sesion")
def catalogo(request):
    #sesiones
    num_visitas = request.session.get('num_visitas',0)
    num_visitas += 1
    request.session['num_visitas'] = num_visitas

    contexto = {
        'num_visitas':num_visitas,
    }

    return render(request, "catalogo/catalogo.html",contexto)

with open("bibliotecas.txt","r") as f:
        lista_urls=f.read().split("\n")


def buscar_libros(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        urls=[f'http://{u}/api/libros/?search={query}' for u in lista_urls]
        """urls = [
            f'http://127.0.0.1:8001/api/libros/?search={query}',
            f'http://127.0.0.1:8002/api/libros/?search={query}',
        ]"""
        for url in urls:
            try:
                response = httpx.get(url, timeout=10.0)
                if response.status_code == 200:
                    resultados.extend(response.json())  # Añade los libros de esta biblioteca
            except httpx.RequestError:
                pass  # Ignora errores de conexión

    return render(request, 'catalogo/catalogo.html', {
        'resultados': resultados,
        'query': query
    })


"""class LibroListView(generic.ListView):
    model = Libro
    paginate_by = 10
class LibroDetailView(generic.DetailView):
    model = Libro
    template_name = 'catalogo/detalles_libro.html'
class AutorListView(generic.ListView):
    model = Autor
    paginate_by = 10
class AutorDetailView(generic.DetailView):
    model = Autor
    template_name = 'catalogo/detalles_autor.html'"""