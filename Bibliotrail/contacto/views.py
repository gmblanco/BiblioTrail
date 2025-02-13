from django.shortcuts import render, redirect
from .forms import FormularioContacto
from django.core.mail import EmailMessage

def contacto(request):
    form = FormularioContacto()  # Inicializa el formulario antes de la lógica de la vista
    if request.method == "POST":
        form = FormularioContacto(data = request.POST)
        if form.is_valid():
            # Procesa los datos del formulario
            nombre = request.POST.get("nombre")
            primer_apellido = request.POST.get("primer_apellido")
            segundo_apellido = request.POST.get("segundo_apellido")
            email = request.POST.get("email")
            telefono = request.POST.get("telefono")
            asunto = request.POST.get("asunto")
            categoria = request.POST.get("categoria")
            mensaje = request.POST.get("mensaje")

            contenido = f"""
            📩 Nuevo mensaje de contacto recibido
            
            Nombre: {nombre} {primer_apellido} {segundo_apellido}
            Correo Electrónico: {email}
            Teléfono: {telefono}
            Categoría: {categoria}

            Mensaje:
            {mensaje}
            """

            email = EmailMessage(asunto,contenido,"",["gm58@illinois.edu"],reply_to=[email])

            try:
                email.send()
                print(form.cleaned_data)  # Esto solo imprime los datos por ahora
                #return redirect(f'{reverse("Contacto")}?valido')  # Redirige a la misma página con el parámetro 'valido'
                return redirect('/contacto/?valido')
            except:
                return redirect('/contacto/?invalido')

    return render(request, "contacto/contacto.html", {"form": form})
