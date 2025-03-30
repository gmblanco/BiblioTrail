from django.shortcuts import render
from django.conf import settings
import os
import requests

def inicio(request):

    return render(request, "BibliotrailApp/inicio.html")

def eventos(request):
    
    return render(request, "BibliotrailApp/eventos.html")

def reservas(request):
    
    return render(request, "BibliotrailApp/reservas.html")
