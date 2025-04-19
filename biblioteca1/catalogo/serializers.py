from rest_framework.serializers import ModelSerializer
from .models import *

class IdiomaSerializer(ModelSerializer):
    class Meta:
        model = Idioma
        fields = '__all__'

class GeneroSerializer(ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class LibroSerializer(ModelSerializer):
    autor = AutorSerializer()
    genero = GeneroSerializer(many=True)
    idioma = IdiomaSerializer()
    class Meta:
        model = Libro
        fields = '__all__'

class EjemplarSerializer(ModelSerializer):
    libro = LibroSerializer()
    class Meta:
        model = EjemplarLibro
        fields = '__all__'

class BibliotecaSerializer(ModelSerializer):
    class Meta:
        model = Biblioteca
        fields = '__all__'

class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class EspacioSerializer(ModelSerializer):
    class Meta:
        model = Espacio
        fields = '__all__'