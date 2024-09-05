import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from .models import Rutina, TipoDeRutina, Usuario, Cliente, Instructor, Objetivo, InformacionPersonalInstructor, Horario
from django.utils.dateparse import parse_date
import io
from datetime import datetime, timedelta

def index(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(Username=username)
            
            # Verificación de contraseña sin hash
            if password == usuario.Password and usuario.Tipo == "Cliente":
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
        rutinas = Rutina.objects.filter(Nombre__icontains=query)
    else:
        rutinas = Rutina.objects.all()
    
    if not rutinas:
        mensaje = "No se encontraron rutinas."
    else:
        mensaje = None
    
    return render(request, "gestionRutinas.html", {"rutinas": rutinas, "mensaje": mensaje})

def visualizarRutina(request, id):
    # Obtener la instancia de Rutina usando el ID proporcionado
    rutina = get_object_or_404(Rutina, RutinaID=id)
    
    # Obtener los objetivos asociados a la rutina
    objetivos = Objetivo.objects.filter(RutinaID=rutina)
    
    # Obtener los datos adicionales necesarios para mostrar en la plantilla
    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    # Renderizar la plantilla con los datos necesarios
    return render(request, "visualizarRutina.html", {
        "rutina": rutina,
        "objetivos": objetivos,
        "instructores": instructores,
        "tipos": tipos,
        "clientes": clientes
    })

def registrarRutina(request):
    if request.method == "POST":
        nombre = request.POST.get('Nombre')
        tipo_id = request.POST.get('TipoID')
        descripcion = request.POST.get('Descripcion')
        frecuencia = request.POST.get('Frecuencia')
        fecha_inicio = request.POST.get('FechaInicio')
        fecha_fin = request.POST.get('FechaFin')
        imagen = request.FILES.get('Imagen')
        instructor_id = request.POST.get('InstructorID')
        cliente_id = request.POST.get('ClienteID')

        if imagen:
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            imagen_nombre = file_name
        else:
            imagen_nombre = None

        rutina = Rutina.objects.create(
            Nombre=nombre,
            TipoID_id=tipo_id,
            Descripcion=descripcion,
            Frecuencia=frecuencia,
            FechaInicio=parse_date(fecha_inicio),
            FechaFin=parse_date(fecha_fin),
            Imagen=imagen_nombre,
            InstructorID_id=instructor_id,
            ClienteID_id=cliente_id
        )

        # Crear Objetivos asociados a la rutina
        i = 0
        while True:
            nombre_objetivo = request.POST.get(f'ObjetivosNombre{i}')
            if not nombre_objetivo:
                break

            estado_inicial = float(request.POST.get(f'ObjetivosEstadoInicial{i}', 0.0))
            estado_final = float(request.POST.get(f'ObjetivosEstadoFinal{i}', 0.0))

            Objetivo.objects.create(
                Nombre=nombre_objetivo,
                EstadoInicial=estado_inicial,
                EstadoFinal=estado_final,
                RutinaID=rutina
            )

            i += 1

        return redirect('gestionRutinas')

    # instructores = Instructor.objects.all()
    instructores = []
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    frecuencias = []

    return render(request, "registrarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos,
        "clientes": clientes,
        "frecuencias": frecuencias
    })

def editarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    
    if request.method == "POST":
        nombre = request.POST.get('Nombre')
        tipo_id = request.POST.get('TipoID')
        descripcion = request.POST.get('Descripcion')
        frecuencia = request.POST.get('Frecuencia')
        fecha_inicio = request.POST.get('FechaInicio')
        fecha_fin = request.POST.get('FechaFin')
        imagen = request.FILES.get('Imagen')
        instructor_id = request.POST.get('InstructorID')
        cliente_id = request.POST.get('ClienteID')

        # Initialize variables
        instructor = None
        cliente = None

        # Obtener instancias de Instructor y Cliente
        try:
            instructor = Instructor.objects.get(InstructorID=instructor_id)
            cliente = Cliente.objects.get(ClienteID=cliente_id)
        except Instructor.DoesNotExist:
            instructor = None
        except Cliente.DoesNotExist:
            cliente = None

        rutina.Nombre = nombre
        rutina.TipoID_id = tipo_id
        rutina.Descripcion = descripcion
        rutina.Frecuencia = frecuencia
        rutina.FechaInicio = parse_date(fecha_inicio)
        rutina.FechaFin = parse_date(fecha_fin)

        if imagen:
            image = Image.open(imagen)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            rutina.Imagen = file_name

        rutina.InstructorID = instructor
        rutina.ClienteID = cliente
        rutina.save()

        # Eliminar Objetivos existentes antes de añadir los nuevos
        Objetivo.objects.filter(RutinaID=rutina).delete()

        # Crear Objetivos asociados a la rutina
        i = 0
        while True:
            nombre_objetivo = request.POST.get(f'ObjetivosNombre{i}')
            if not nombre_objetivo:
                break

            estado_inicial = float(request.POST.get(f'ObjetivosEstadoInicial{i}', 0.0))
            estado_final = float(request.POST.get(f'ObjetivosEstadoFinal{i}', 0.0))

            Objetivo.objects.create(
                Nombre=nombre_objetivo,
                EstadoInicial=estado_inicial,
                EstadoFinal=estado_final,
                RutinaID=rutina
            )

            i += 1

        return redirect('gestionRutinas')

    tipo_id = rutina.TipoID.EspecialidadID.EspecialidadID
    tipo_rutina = TipoDeRutina.objects.get(pk=tipo_id)
    especialidad_id = tipo_rutina.EspecialidadID_id
    instructores = Instructor.objects.filter(Especialidad__EspecialidadID=especialidad_id).distinct()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    # Obtener frecuencias basadas en el instructor actual
    frecuencias = []
    if rutina.InstructorID:
        horarios = Horario.objects.filter(InstructorID=rutina.InstructorID)
        frecuencias = [
            f"{horario.Dia}: {horario.HoraInicio.strftime('%H:%M')} - {horario.HoraFin.strftime('%H:%M')}"
            for horario in horarios
        ]

    # Obtener los objetivos asociados a la rutina
    objetivos = Objetivo.objects.filter(RutinaID=rutina)

    # Obtener los objetivos asociados a la rutina
    objetivos = Objetivo.objects.filter(RutinaID=rutina)

    return render(request, "editarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos, 
        "clientes": clientes,
        "rutina": rutina,
        "frecuencias": frecuencias,
        "objetivos": objetivos
    })


def eliminarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    rutina.delete()
    return redirect('gestionRutinas')


from django.http import JsonResponse

def obtener_instructores_por_especialidad(request):
    tipo_rutina_id = request.GET.get('tipo_rutina_id')
    
    # Obtener la especialidad del tipo de rutina seleccionado
    tipo_rutina = TipoDeRutina.objects.get(pk=tipo_rutina_id)
    especialidad_id = tipo_rutina.EspecialidadID_id

    # Filtrar instructores por la especialidad
    instructores = Instructor.objects.filter(Especialidad__EspecialidadID=especialidad_id).distinct()

    # Construir la respuesta en formato JSON
    instructores_data = [
        {'id': instructor.InstructorID, 'nombre': f"{instructor.Nombres} {instructor.Apellidos}"}
        for instructor in instructores
    ]
    
    return JsonResponse(instructores_data, safe=False)


def obtener_frecuencias_por_instructor(request):
    instructor_id = request.GET.get('instructor_id')

    # Obtener el instructor seleccionado y sus horarios
    instructor = Instructor.objects.get(pk=instructor_id)
    horarios = Horario.objects.filter(InstructorID=instructor)

    # Construir la lista de frecuencias formateadas
    frecuencias_data = [
        f"{horario.Dia}: {horario.HoraInicio.strftime('%H:%M')} - {horario.HoraFin.strftime('%H:%M')}"
        for horario in horarios
    ]

    # Construir la respuesta en formato JSON
    return JsonResponse(frecuencias_data, safe=False)

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

def obtener_rangos_de_fechas(request):
    instructor_id = request.GET.get('instructor_id')
    frecuencia = request.GET.get('frecuencia')

    if not instructor_id or not frecuencia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    # Obtener todas las rutinas con la misma frecuencia, horario e instructor
    rutinas = Rutina.objects.filter(
        InstructorID=instructor_id, 
        Frecuencia=frecuencia, 
        FechaFin__gte=datetime.now().date()
    ).order_by('FechaInicio')

    rangos_de_fechas = []
    for rutina in rutinas:
        fecha_fin_mas_un_dia = rutina.FechaFin + timedelta(days=1)
        rangos_de_fechas.append({
            'fecha_inicio': rutina.FechaInicio.strftime('%Y-%m-%d'),
            'fecha_fin': fecha_fin_mas_un_dia.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'rangos_de_fechas': rangos_de_fechas})

from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Rutina  # Ajusta esto según tu estructura de proyecto

def obtener_rangos_de_fechas_excluyendo(request):
    instructor_id = request.GET.get('instructor_id')
    frecuencia = request.GET.get('frecuencia')
    rutina_id = request.GET.get('rutina_id')  # ID de la rutina que se está editando

    if not instructor_id or not frecuencia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    # Obtener todas las rutinas con la misma frecuencia, horario e instructor
    # Excluir la rutina actual que se está editando
    rutinas = Rutina.objects.filter(
        InstructorID=instructor_id,
        Frecuencia=frecuencia,
        FechaFin__gte=datetime.now().date()
    ).exclude(RutinaID=rutina_id).order_by('FechaInicio')

    rangos_de_fechas = []
    for rutina in rutinas:
        fecha_fin_mas_un_dia = rutina.FechaFin + timedelta(days=1)
        rangos_de_fechas.append({
            'fecha_inicio': rutina.FechaInicio.strftime('%Y-%m-%d'),
            'fecha_fin': fecha_fin_mas_un_dia.strftime('%Y-%m-%d'),
        })

    return JsonResponse({'rangos_de_fechas': rangos_de_fechas})
