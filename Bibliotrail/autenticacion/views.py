# views.py
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegistroForm

class VistaRegistro(View):
    def get(self, request):
        form = RegistroForm()
        return render(request, "registro/registro.html", {"form": form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.first_name = form.cleaned_data['nombre']  # Asignamos el nombre al campo first_name
            usuario.last_name = form.cleaned_data['apellidos']  # Asignamos los apellidos al campo last_name
            # Verificar si el tipo de usuario es "Bibliotecario" y asignar is_staff
            if form.cleaned_data['tipo_usuario'] == 'bibliotecario':
                usuario.is_staff = True
            else:
                usuario.is_staff = False
            usuario.save()
            login(request, usuario)
            return redirect("Inicio")
        else:
            for mensaje in form.error_messages:
                messages.error(request, form.error_messages[mensaje])
            return render(request, "registro/registro.html", {"form": form})
      
def cerrar_sesion(request):
    logout(request)
    return redirect("Inicio")