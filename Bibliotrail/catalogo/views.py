from django.shortcuts import render
import httpx
from django.shortcuts import render
from .models import Libro, Autor, EjemplarLibro, Genero, Idioma
from django.views import generic
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="iniciar_sesion")
def catalogo(request):
    num_libros = Libro.objects.all().count()
    num_ejemplares = EjemplarLibro.objects.all().count()
    num_ejemplares_disponibles = EjemplarLibro.objects.filter(estado__exact='d').count()
    num_autores = Autor.objects.count()
    num_generos = Genero.objects.count()
    num_idiomas = Idioma.objects.count()
    
    #sesiones
    num_visitas = request.session.get('num_visitas',0)
    num_visitas += 1
    request.session['num_visitas'] = num_visitas

    contexto = {
        'num_libros':num_libros,
        'num_ejemplares':num_ejemplares,
        'num_ejemplares_disponibles':num_ejemplares_disponibles,
        'num_autores':num_autores,
        'num_generos':num_generos,
        'num_idiomas':num_idiomas,
        'num_visitas':num_visitas,
    }

    return render(request, "catalogo/catalogo.html",contexto)

class LibroListView(generic.ListView):
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
    template_name = 'catalogo/detalles_autor.html'

def buscar_libros(request):
    query = request.GET.get('q', '')
    resultados = []

    if query:
        urls = [
            f'http://127.0.0.1:8001/api/libros/?search={query}',
            f'http://127.0.0.1:8002/api/libros/?search={query}',
        ]
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