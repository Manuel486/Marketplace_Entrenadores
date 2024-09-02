import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from .models import Rutina, TipoDeRutina, Instructor, Cliente, Usuario, InformacionPersonalInstructor
from django.utils.dateparse import parse_date
import io

def index(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(Username=username)
            if password == usuario.Password and usuario.Tipo == "Cliente":
                return redirect('menu')
            else:
                return render(request, 'login.html', {'error': 'Usuario o contraseña no válidos'})
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o contraseña no válidos'})

    return render(request, 'login.html')

def menu(request):
    return render(request, 'menu.html')

def gestionRutinas(request):
    query = request.GET.get('search', '')
    
    if query:
        rutinas = Rutina.objects.filter(Nombre__icontains=query)
    else:
        rutinas = Rutina.objects.all()
    
    mensaje = "No se encontraron rutinas." if not rutinas else None
    
    return render(request, "gestionRutinas.html", {"rutinas": rutinas, "mensaje": mensaje})

def visualizarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)
    return render(request, "visualizarRutina.html", {"rutina": rutina})

def registrarRutina(request):
    if request.method == "POST":
        nombre = request.POST.get('txtNombre')
        tipo_id = request.POST.get('txtTipo')
        descripcion = request.POST.get('txtDescripcion')
        frecuencia = request.POST.get('txtFrecuencia')
        fecha_inicio = request.POST.get('txtFechaInicio')
        fecha_fin = request.POST.get('txtFechaFin')
        imagen = request.FILES.get('txtImagen')
        horas_recomendadas = request.POST.get('txtHorasRecomendadas')
        objetivos = request.POST.get('txtObjetivos')
        instructor_id = request.POST.get('txtInstructor')
        cliente_id = request.POST.get('txtCliente')
        print("El valor del id es: ",cliente_id)

        # Procesar la imagen
        imagen_nombre = None
        if imagen:
            unique_id = uuid.uuid4().hex
            file_extension = imagen.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')
            default_storage.save(file_name, thumb_io)
            imagen_nombre = file_name

        rutina = Rutina.objects.create(
            Nombre=nombre,
            TipoID_id=tipo_id,
            Descripcion=descripcion,
            Frecuencia=frecuencia,
            FechaInicio=parse_date(fecha_inicio),
            FechaFin=parse_date(fecha_fin),
            Imagen=imagen_nombre,
            HorasRecomendadas=horas_recomendadas,
            Objetivos=objetivos,
            InstructorID_id=instructor_id,
            ClienteID_id=cliente_id  # Usar ID del cliente aquí
        )

        return redirect('gestionRutinas')

    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()

    frecuencias = {}
    for instructor in instructores:
        try:
            info_personal = InformacionPersonalInstructor.objects.get(InstructorID=instructor)
            frecuencias[instructor.InstructorID] = info_personal.PreferenciaHorario
        except InformacionPersonalInstructor.DoesNotExist:
            frecuencias[instructor.InstructorID] = "No disponible"

    return render(request, "registrarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos,
        "clientes": clientes,
        "frecuencias": frecuencias
    })

def editarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)

    if request.method == "POST":
        nombre = request.POST.get('txtNombre')
        tipo_id = request.POST.get('txtTipo')
        descripcion = request.POST.get('txtDescripcion')
        fecha_inicio = request.POST.get('txtFechaInicio')
        fecha_fin = request.POST.get('txtFechaFin')
        imagen = request.FILES.get('txtImagen')
        horas_recomendadas = request.POST.get('txtHorasRecomendadas')
        objetivos = request.POST.get('txtObjetivos')
        instructor_id = request.POST.get('txtInstructor')
        cliente_id = request.POST.get('txtCliente')

        rutina.Nombre = nombre
        rutina.TipoID_id = tipo_id
        rutina.Descripcion = descripcion
        rutina.FechaInicio = parse_date(fecha_inicio)
        rutina.FechaFin = parse_date(fecha_fin)

        if imagen:
            unique_id = uuid.uuid4().hex
            file_extension = imagen.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')
            default_storage.save(file_name, thumb_io)
            rutina.Imagen = file_name

        rutina.Frecuencia = horas_recomendadas
        rutina.HorasRecomendadas = horas_recomendadas
        rutina.Objetivos = objetivos
        rutina.InstructorID_id = instructor_id
        rutina.ClienteID_id = cliente_id
        rutina.save()

        return redirect('gestionRutinas')

    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()

    frecuencias = {instructor.Informacionpersonalinstructor_set.first().PreferenciaHorario if instructor.Informacionpersonalinstructor_set.exists() else 'No disponible' for instructor in instructores}

    return render(request, "editarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos, 
        "clientes": clientes,
        "rutina": rutina,
        "frecuencias": frecuencias
    })

def eliminarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)
    rutina.delete()
    return redirect('gestionRutinas')
