from django.shortcuts import render
from rest_framework import generics
from .models import Libro
from .serializers import LibroSerializer
from rest_framework.filters import SearchFilter

class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends = [SearchFilter]
    search_fields = ['titulo', 'autor__nombre', 'autor__apellidos']
