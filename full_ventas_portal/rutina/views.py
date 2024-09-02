import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from .models import Rutina, Frecuencia, Instructor, TipoDeRutina, Usuario, Cliente
from django.utils.dateparse import parse_date
import io

def index(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(username=username)
            
            # Verificación de contraseña sin hash
            if password == usuario.password and usuario.rol == "Administrador":
                return redirect('menu')
            else:
                return render(request, 'login.html', {'error': 'Usuario o contraseña no válido'})

        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o contraseña no válido'})

    return render(request, 'login.html')

def menu(request):
    return render(request, 'menu.html')

def gestionRutinas(request):
    query = request.GET.get('search', '')
    
    if query:
        rutinas = Rutina.objects.filter(nombre__icontains=query)
    else:
        rutinas = Rutina.objects.all()
    
    if not rutinas:
        mensaje = "No se encontraron rutinas."
    else:
        mensaje = None
    
    return render(request, "gestionRutinas.html", {"rutinas": rutinas, "mensaje": mensaje})

def visualizarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)

    return render(request, "visualizarRutina.html", {"rutina": rutina})


def registrarRutina(request):
    if request.method == "POST":
        nombre = request.POST.get('txtNombre')
        tipo_id = request.POST.get('txtTipo') 
        descripcion = request.POST.get('txtDescripcion')
        frecuencia_id = request.POST.get('txtFrecuencia')
        fecha_inicio = request.POST.get('txtFechaInicio')
        fecha_fin = request.POST.get('txtFechaFin')
        imagen = request.FILES.get('txtImagen')
        dias_recomendados = request.POST.get('txtDiasRecomendados')
        objetivos = request.POST.get('txtObjetivos')
        instructor_id = request.POST.get('txtInstructor')
        cliente_id = request.POST.get('txtCliente')

        if imagen:
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')
            
            unique_id = uuid.uuid4().hex  # Genera un ID único en formato hexadecimal
            file_extension = imagen.name.split('.')[-1]  # Obtiene la extensión del archivo original
            file_name = f'{unique_id}.{file_extension}'  # Nombre del archivo con extensión
            
            # Guardar el archivo
            thumb_file = default_storage.save(file_name, thumb_io)
            
            # Guardar solo el nombre del archivo con extensión
            imagen_nombre = file_name
        else:
            imagen_nombre = None

        Rutina.objects.create(
            nombre=nombre,
            tipo_id=tipo_id,
            descripcion=descripcion,
            frecuencia_id=frecuencia_id,
            fecha_inicio=parse_date(fecha_inicio),
            fecha_fin=parse_date(fecha_fin),
            imagen=imagen_nombre,
            dias_recomendados=dias_recomendados,
            objetivos=objetivos,
            instructor_id=instructor_id,
            cliente_id=cliente_id
        )
        return redirect('gestionRutinas')

    frecuencias = Frecuencia.objects.all()
    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    return render(request, "registrarRutina.html", {
        "frecuencias": frecuencias, 
        "instructores": instructores, 
        "tipos": tipos,
        "clientes": clientes
    })

def editarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)

    if request.method == "POST":
        nombre = request.POST.get('txtNombre')
        tipo_id = request.POST.get('txtTipo')
        descripcion = request.POST.get('txtDescripcion')
        frecuencia_id = request.POST.get('txtFrecuencia')
        fecha_inicio = request.POST.get('txtFechaInicio')
        fecha_fin = request.POST.get('txtFechaFin')
        imagen = request.FILES.get('txtImagen')
        dias_recomendados = request.POST.get('txtDiasRecomendados')
        objetivos = request.POST.get('txtObjetivos')
        instructor_id = request.POST.get('txtInstructor')
        cliente_id = request.POST.get('txtCliente')

        rutina.nombre = nombre
        rutina.tipo_id = tipo_id
        rutina.descripcion = descripcion
        rutina.frecuencia_id = frecuencia_id
        rutina.fecha_inicio = parse_date(fecha_inicio)
        rutina.fecha_fin = parse_date(fecha_fin)

        if imagen:
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            # Generar un nombre de archivo único usando UUID
            unique_id = uuid.uuid4().hex
            file_extension = imagen.name.split('.')[-1]  # Obtener la extensión del archivo original
            file_name = f'{unique_id}.{file_extension}'  # Nombre del archivo con extensión
            
            # Guardar el archivo y obtener solo el nombre del archivo
            default_storage.save(file_name, thumb_io)
            rutina.imagen = file_name  # Solo guardar el nombre del archivo

        rutina.dias_recomendados = dias_recomendados
        rutina.objetivos = objetivos
        rutina.instructor_id = instructor_id
        rutina.cliente_id = cliente_id
        rutina.save()

        return redirect('gestionRutinas')

    frecuencias = Frecuencia.objects.all()
    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    return render(request, "editarRutina.html", {
        "frecuencias": frecuencias, 
        "instructores": instructores, 
        "tipos": tipos, 
        "clientes": clientes,
        "rutina": rutina
    })

def eliminarRutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)
    rutina.delete()
    return redirect('gestionRutinas')
