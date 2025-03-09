from rest_framework.decorators import api_view
from rest_framework.response import Response
from catalogo.models import Libro, Autor
from .serializers import *

@api_view(['GET'])
def getRutas(request):
    rutas = [
        'GET /api',
        'GET /api/libros'
    ]
    return Response(rutas)

@api_view(['GET'])
def getLibros(request):
    libros = Libro.objects.all()
    serializer = LibroSerializer(libros, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getAutores(request):
    autores = Autor.objects.all()
    serializer = AutorSerializer(autores, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getEjemplares(request):
    ejemplares = EjemplarLibro.objects.all()
    serializer = EjemplarSerializer(ejemplares, many = True)
    return Response(serializer.data)