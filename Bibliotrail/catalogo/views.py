from django.shortcuts import render
from .models import Libro, Autor, EjemplarLibro, Genero, Idioma, PerfilUsuario, Prestamo
from django.views import generic
#from django.contrib.auth.mixins import LoginRequiredMixin

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

"""
class PrestamosUsuarioListView(LoginRequiredMixin, generic.ListView):
    ""
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    ""
    model = Prestamo
    template_name ='catalog/prestamos_usuario.html'
    paginate_by = 10

    def get_queryset(self):
        return Prestamo.objects.filter(usuario__user=self.request.user).exclude(estado ='c').order_by('fecha_prestamo')"""