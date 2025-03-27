from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
import re
from .models import PerfilUsuario

class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
  

    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)

        # Asignar clase form-control a todos los campos del formulario
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['avatar','username', 'email', 'nombre', 'apellido', 'dni', 'direccion', 'codigo_postal','ciudad','provincia','bio']

    # Asignar clases de Bootstrap directamente a los widgets
    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        
        # Asignar clase form-control a todos los campos del formulario
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                # Verificar si el username existe en la base de datos
                from django.contrib.auth.models import User
                if User.objects.filter(username=username).exists():
                    self.add_error('password', "La contraseña es incorrecta.")
                else:
                    self.add_error('username', "El nombre de usuario no existe.")
        
        return self.cleaned_data
