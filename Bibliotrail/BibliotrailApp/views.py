from django.shortcuts import render


# Create your views here.

def inicio(request):

    return render(request, "BibliotrailApp/inicio.html")

def novedades(request):
    
    return render(request, "BibliotrailApp/novedades.html")

def eventos(request):
    
    return render(request, "BibliotrailApp/eventos.html")

def reservas(request):
    
    return render(request, "BibliotrailApp/reservas.html")

