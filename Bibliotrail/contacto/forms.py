from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(
        label="Nombre", 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    primer_apellido = forms.CharField(
        label="Primer Apellido", 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    segundo_apellido = forms.CharField(
        label="Segundo Apellido", 
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="E-mail", 
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    telefono = forms.CharField(
        label="Teléfono", 
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+34 123456789"})
    )
    asunto = forms.CharField(
        label="Asunto", 
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    categoria = forms.ChoiceField(
        label="¿De qué se trata?",
        required=True,
        choices=[
            ('problema', 'Problema'),
            ('consulta', 'Consulta'),
            ('queja', 'Queja'),
            ('sugerencia', 'Sugerencia'),
            ('agradecimiento', 'Agradecimiento'),
        ],
        widget=forms.Select(attrs={"class": "form-select"})  # Select de Bootstrap
    )
    mensaje = forms.CharField(
        label="Mensaje", 
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )
