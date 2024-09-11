import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from .models import Rutina, TipoDeRutina, Usuario, Cliente, Instructor, Meta, Horario,MetaPredeterminada
from django.utils.dateparse import parse_date
import io
from datetime import datetime, timedelta
from decimal import Decimal

def index(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(Username=username)
            
            if password == usuario.Password and usuario.Tipo == "Cliente":
                return redirect('gestionRutinas')
            else:
                return render(request, 'auth/login.html', {'error': 'Usuario o contraseña no válido'})

        except Usuario.DoesNotExist:
            return render(request, 'auth/login.html', {'error': 'Usuario o contraseña no válido'})

    return render(request, 'auth/login.html')

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

    for rutina in rutinas:
        imagen1 = rutina.Imagen1
        if imagen1 and imagen1.name:
            print(f"Rutina ID: {rutina.RutinaID}")
            print("URL:", imagen1.url)
            print("Nombre:", imagen1.name)
            print("Path:", imagen1.path)
        else:
            print(f"Rutina ID: {rutina.RutinaID} no tiene imagen1 asociada.")
        print("-----")
    return render(request, "admin/gestionRutinas.html", {"rutinas": rutinas, "mensaje": mensaje})

def visualizarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    
    metas = Meta.objects.filter(RutinaID=rutina)

    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    return render(request, "admin/visualizarRutina.html", {
        "rutina": rutina,
        "metas": metas,
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
        imagen1 = request.FILES.get('Imagen1')
        imagen2 = request.FILES.get('Imagen2')
        instructor_id = request.POST.get('InstructorID')
        cliente_id = request.POST.get('ClienteID')
        objetivos = request.POST.get('Objetivos')

        if imagen1:
            image = Image.open(imagen1)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen1.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            imagen_nombre1 = file_name
        else:
            imagen_nombre1 = None

        if imagen2:
            image = Image.open(imagen2)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen2.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            imagen_nombre2 = file_name
        else:
            imagen_nombre2 = None

        rutina = Rutina.objects.create(
            Nombre=nombre,
            TipoID_id=tipo_id,
            Descripcion=descripcion,
            Frecuencia=frecuencia,
            FechaInicio=parse_date(fecha_inicio),
            FechaFin=parse_date(fecha_fin),
            Imagen1=imagen_nombre1,
            Imagen2=imagen_nombre2,
            InstructorID_id=instructor_id,
            ClienteID_id=cliente_id,
            Objetivos = objetivos
        )

        i = 0
        while True:
            nombre_meta = request.POST.get(f'MetaNombre{i}')
            print("LA META ES:::",nombre_meta)
            if not nombre_meta:
                break

            estado_inicial = Decimal(request.POST.get(f'MetaEstadoInicial{i}'))
            estado_final = Decimal(request.POST.get(f'MetaEstadoFinal{i}'))

            Meta.objects.create(
                Nombre=nombre_meta,
                EstadoInicial=estado_inicial,
                EstadoFinal=estado_final,
                RutinaID=rutina
            )

            i += 1

        return redirect('gestionRutinas')

    instructores = []
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    frecuencias = []

    return render(request, "admin/registrarRutina.html", {
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
        imagen1 = request.FILES.get('Imagen1')
        imagen2 = request.FILES.get('Imagen2')
        instructor_id = request.POST.get('InstructorID')
        cliente_id = request.POST.get('ClienteID')
        objetivos = request.POST.get('Objetivos')

        instructor = None
        cliente = None
        
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

        if imagen1:
            image = Image.open(imagen1)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen1.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            rutina.Imagen1 = file_name
        else:
            rutina.Imagen1 = None

        if imagen2:
            image = Image.open(imagen2)
            image = image.convert('RGB')
            thumb_io = io.BytesIO()
            image.save(thumb_io, 'JPEG')

            unique_id = uuid.uuid4().hex
            file_extension = imagen2.name.split('.')[-1]
            file_name = f'{unique_id}.{file_extension}'
            
            default_storage.save(file_name, thumb_io)
            rutina.Imagen2 = file_name
        else:
            rutina.Imagen2 = None

        rutina.InstructorID = instructor
        rutina.ClienteID = cliente
        rutina.Objetivos = objetivos
        rutina.save()

        Meta.objects.filter(RutinaID=rutina).delete()

        i = 0
        while True:
            nombre_meta = request.POST.get(f'MetaNombre{i}')
            if not nombre_meta:
                break

            estado_inicial = Decimal(request.POST.get(f'MetaEstadoInicial{i}'))
            estado_final = Decimal(request.POST.get(f'MetaEstadoFinal{i}'))

            Meta.objects.create(
                Nombre=nombre_meta,
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
    
    frecuencias = []
    if rutina.InstructorID:
        horarios = Horario.objects.filter(InstructorID=rutina.InstructorID)
        frecuencias = [
            f"{horario.Dia}: {horario.HoraInicio.strftime('%H:%M')} - {horario.HoraFin.strftime('%H:%M')}"
            for horario in horarios
        ]

    metas = Meta.objects.filter(RutinaID=rutina)

    return render(request, "admin/editarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos, 
        "clientes": clientes,
        "rutina": rutina,
        "frecuencias": frecuencias,
        "metas": metas
    })


def eliminarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    rutina.delete()
    return redirect('gestionRutinas')


from django.http import JsonResponse

from django.http import JsonResponse
from .models import MetaPredeterminada

def obtener_metas_por_tipo_de_rutina(request):
    tipo_rutina_id = request.GET.get('tipo_rutina_id')

    if tipo_rutina_id:
        metas_predeterminadas = MetaPredeterminada.objects.filter(TipoDeRutinaID_id=tipo_rutina_id).distinct()
        
        metas_por_rutina_data = [
            {'id': meta_predeterminada.MetaPredeterminadaID, 'nombre': meta_predeterminada.Nombre}
            for meta_predeterminada in metas_predeterminadas
        ]
        
        return JsonResponse(metas_por_rutina_data, safe=False)
    else:
        return JsonResponse([], safe=False)

    
def obtener_instructores_por_especialidad(request):
    tipo_rutina_id = request.GET.get('tipo_rutina_id')
    
    tipo_rutina = TipoDeRutina.objects.get(pk=tipo_rutina_id)
    especialidad_id = tipo_rutina.EspecialidadID_id

    instructores = Instructor.objects.filter(Especialidad__EspecialidadID=especialidad_id).distinct()

    instructores_data = [
        {'id': instructor.InstructorID, 'nombre': f"{instructor.Nombres} {instructor.Apellidos}"}
        for instructor in instructores
    ]
    
    return JsonResponse(instructores_data, safe=False)


def obtener_frecuencias_por_instructor(request):
    instructor_id = request.GET.get('instructor_id')

    instructor = Instructor.objects.get(pk=instructor_id)
    horarios = Horario.objects.filter(InstructorID=instructor)

    frecuencias_data = [
        f"{horario.Dia}: {horario.HoraInicio.strftime('%H:%M')} - {horario.HoraFin.strftime('%H:%M')}"
        for horario in horarios
    ]

    return JsonResponse(frecuencias_data, safe=False)

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta

def obtener_rangos_de_fechas(request):
    instructor_id = request.GET.get('instructor_id')
    frecuencia = request.GET.get('frecuencia')

    if not instructor_id or not frecuencia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

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
from .models import Rutina 

def obtener_rangos_de_fechas_excluyendo(request):
    instructor_id = request.GET.get('instructor_id')
    frecuencia = request.GET.get('frecuencia')
    rutina_id = request.GET.get('rutina_id')  

    if not instructor_id or not frecuencia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

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
