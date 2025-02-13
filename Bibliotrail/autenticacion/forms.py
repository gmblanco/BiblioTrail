from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class RegistroForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dni = forms.CharField(max_length=9, min_length=9, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.ChoiceField(choices=[('M', 'Hombre'), ('F', 'Mujer')], widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_usuario = forms.ChoiceField(choices=[('usuario', 'Usuario'), ('bibliotecario', 'Bibliotecario')], widget=forms.Select(attrs={'class': 'form-control'}))

    # Dirección detallada
    calle = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    codigo_postal = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ciudad = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    provincia = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

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
