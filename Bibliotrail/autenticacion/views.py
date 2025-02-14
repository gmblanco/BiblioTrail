# views.py
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from catalogo.models import PerfilUsuario

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

            """
            # Crear el perfil asociado
            PerfilUsuario.objects.create(
                user=usuario,
                dni=form.cleaned_data.get("dni"),
                sexo=form.cleaned_data.get("sexo"),
                direccion=form.cleaned_data.get("direccion"),
                codigo_postal=form.cleaned_data.get("codigo_postal"),
                ciudad=form.cleaned_data.get("ciudad"),
                provincia=form.cleaned_data.get("provincia"),
            )"""

            login(request, usuario)
            return redirect("Inicio")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, "registro/registro.html", {"form": form})
            
      
def cerrar_sesion(request):
    logout(request)
    return redirect("Inicio")

def iniciar_sesion(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)  # Usa tu formulario personalizado
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Inicio")
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")  # Mensajes más específicos

    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})
