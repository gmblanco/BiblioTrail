from django.shortcuts import render
from rest_framework import generics
from .models import Libro
from .serializers import *
from rest_framework.filters import SearchFilter

class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [SearchFilter]
    search_fields = ['titulo', 'autor__nombre', 'autor__apellidos']

class EjemplaresDisponiblesAPIView(generics.ListAPIView):
    serializer_class = EjemplarSerializer

    def get_queryset(self):
        libro_id = self.kwargs['libro_id']
        return EjemplarLibro.objects.filter(libro__id=libro_id, estado='d')