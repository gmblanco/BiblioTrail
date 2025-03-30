import django_filters
from .models import Libro

class LibroFilter(django_filters.FilterSet):
    genero = django_filters.CharFilter(field_name='genero__nombre', lookup_expr='iexact')

    class Meta:
        model = Libro
        fields = ['genero']
