from rest_framework import generics
from .models import Libro
from .serializers import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .filters import LibroFilter

class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'autor__nombre', 'autor__apellidos']
    filterset_class = LibroFilter

class AutorListAPIView(generics.ListAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    search_fields = ['nombre', 'apellidos']

class EventoListAPIView(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['titulo', 'descripcion']

class EventoDetalleAPIView(RetrieveAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

class EjemplaresDisponiblesAPIView(generics.ListAPIView):
    serializer_class = EjemplarSerializer

    def get_queryset(self):
        libro_id = self.kwargs['libro_id']
        return EjemplarLibro.objects.filter(libro__id=libro_id, estado='d')

class LibroDetalleAPIView(APIView):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        ejemplares = EjemplarLibro.objects.filter(libro=libro)

        libro_serializado = LibroSerializer(libro)
        ejemplares_serializados = EjemplarSerializer(ejemplares, many=True)

        return Response({
            "libro": libro_serializado.data,
            "ejemplares": ejemplares_serializados.data
        }, status=status.HTTP_200_OK)
    
class AutorDetalleAPIView(APIView):
    def get(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)

        autor_serializado = AutorSerializer(autor)

        return Response({
            "autor": autor_serializado.data,
        }, status=status.HTTP_200_OK)
    
class EjemplarDetalleAPIView(APIView):
    def get(self, request, pk):
        ejemplar = get_object_or_404(EjemplarLibro, pk=pk)
        serializer = EjemplarSerializer(ejemplar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        ejemplar = get_object_or_404(EjemplarLibro, pk=pk)
        serializer = EjemplarSerializer(ejemplar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BibliotecaInfoAPIView(APIView):
    def get(self, request):
        biblioteca = Biblioteca.objects.first()  # Solo hay una
        serializer = BibliotecaSerializer(biblioteca)
        data = serializer.data
        data["total_libros"] = Libro.objects.count()
        data["total_ejemplares"] = EjemplarLibro.objects.count()
        return Response(data)