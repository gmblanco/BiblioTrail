from django.shortcuts import redirect, render
from catalogo.models import PerfilUsuario
from autenticacion.forms import RegistroUsuarioForm, PerfilForm, LoginForm 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError

def registerPage(request):
    form = RegistroUsuarioForm()

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Guarda y devuelve el usuario creado
            messages.success(request, f'Cuenta creada correctamente para {user.username}')
            
            # Autenticar al usuario con su username y contraseña
            authenticated_user = authenticate(username=user.username, password=request.POST['password1'])

            if authenticated_user is not None:
                login(request, authenticated_user)  # Ahora sí, pasamos un User válido
                return redirect("Inicio")  # Redirige a la página de inicio

    return render(request, 'autenticacion/register.html', {'form': form})

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

def perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    contexto = {'perfil': perfil}
    return render(request, "perfil/perfil.html", contexto)

#@login_required(login_url = 'login')
def editarPerfil(request):
    perfil = request.user.perfil  # Obtener el perfil del usuario
    form = PerfilForm(request.POST or None, request.FILES or None, instance=perfil)  # Manejo de archivos

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            # Validar que el DNI no esté duplicado
            dni = form.cleaned_data.get('dni')
            if PerfilUsuario.objects.filter(dni=dni).exclude(id=perfil.id).exists():
                form.add_error('dni', 'Ya existe Perfil de usuario con este DNI.')
            else:
                form.save()
                return redirect('perfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")  # Mensajes más específicos

    return render(request, "perfil/editar_perfil.html", {'form': form, 'perfil': perfil})

def cerrar_sesion(request):
    logout(request)
    return redirect("Inicio")
