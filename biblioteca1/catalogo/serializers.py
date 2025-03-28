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
    autor = AutorSerializer(many=True)
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