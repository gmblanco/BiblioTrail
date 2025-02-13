from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class RegistroForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = forms.CharField(max_length=9, min_length=9, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=[('M', 'Hombre'), ('F', 'Mujer')], widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_usuario = forms.ChoiceField(required=True,choices=[('usuario', 'Usuario'), ('bibliotecario', 'Bibliotecario')], widget=forms.Select(attrs={'class': 'form-control'}))

    # Dirección detallada
    calle = forms.CharField(required=True, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo_postal = forms.CharField(required=True,max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ciudad = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    provincia = forms.CharField(required=True,max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # 🔥 Añadir estilos Bootstrap a los campos de contraseña
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Repetir contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'nombre', 'apellidos', 'dni', 'sexo', 'calle', 'codigo_postal', 'ciudad', 'provincia','tipo_usuario', 'password1', 'password2']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not re.match(r'^\d{8}[A-Z]$', dni):
            raise forms.ValidationError("El DNI debe tener el formato correcto (8 números seguidos de una letra).")
        return dni

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