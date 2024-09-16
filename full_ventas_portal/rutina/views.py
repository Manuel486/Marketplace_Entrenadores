import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage
from PIL import Image
from .models import Rutina, TipoDeRutina, Usuario, Cliente, Instructor, Meta, MetaPredeterminada, TipoDeRutinaEspecialidad, Especialidad
from django.utils.dateparse import parse_date
import io
from decimal import Decimal
from django.http import JsonResponse

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
    print("gaaa")
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

    return render(request, "admin/rutina/gestionRutinas.html", {"rutinas": rutinas, "mensaje": mensaje})

def visualizarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    
    metas = Meta.objects.filter(RutinaID=rutina)

    instructores = Instructor.objects.all()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    return render(request, "admin/rutina/visualizarRutina.html", {
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

        def procesar_imagen(imagen):
            if imagen:
                image = Image.open(imagen)
                image = image.convert('RGB')
                thumb_io = io.BytesIO()
                image.save(thumb_io, 'JPEG')

                unique_id = uuid.uuid4().hex
                file_extension = imagen.name.split('.')[-1]
                file_name = f'{unique_id}.{file_extension}'

                default_storage.save(file_name, thumb_io)
                return file_name
            return None

        imagen_nombre1 = procesar_imagen(imagen1)
        imagen_nombre2 = procesar_imagen(imagen2)

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
    
    return render(request, "admin/rutina/registrarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos,
        "clientes": clientes
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

        eliminarImagen1 = request.POST.get('EliminarImagen1') == 'true'
        eliminarImagen2 = request.POST.get('EliminarImagen2') == 'true'

        print("EliminarImagen1 : ",eliminarImagen1)
        print("EliminarImagen1 : ",eliminarImagen2)

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
            rutina.Imagen1 = rutina.Imagen1

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
            rutina.Imagen2 = rutina.Imagen2

        if eliminarImagen1:
            rutina.Imagen1 = None
        
        if eliminarImagen2:
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

    tipo_rutina = get_object_or_404(TipoDeRutina, pk=rutina.TipoID_id)
    especialidad_id = TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo_rutina, EspecialidadID__isnull=False).values_list('EspecialidadID', flat=True).first()
    instructores = Instructor.objects.filter(Especialidad__EspecialidadID=especialidad_id).distinct()
    tipos = TipoDeRutina.objects.all()
    clientes = Cliente.objects.all()
    
    
    metas = Meta.objects.filter(RutinaID=rutina)

    return render(request, "admin/rutina/editarRutina.html", {
        "instructores": instructores, 
        "tipos": tipos, 
        "clientes": clientes,
        "rutina": rutina,
        "metas": metas
    })


def eliminarRutina(request, id):
    rutina = get_object_or_404(Rutina, RutinaID=id)
    rutina.delete()
    return redirect('gestionRutinas')


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

    especialidad_id = TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo_rutina).values_list('EspecialidadID', flat=True).first()

    instructores = Instructor.objects.filter(Especialidad__EspecialidadID=especialidad_id).distinct()

    instructores_data = [
        {'id': instructor.InstructorID, 'nombre': f"{instructor.Nombres} {instructor.Apellidos}"}
        for instructor in instructores
    ]
    
    return JsonResponse(instructores_data, safe=False)


def gestionTipoRutinas(request):
    tipos = TipoDeRutina.objects.all()
    return render(request, "admin/tipoDeRutina/gestionTipoDeRutina.html", {"tipos": tipos})

def registrarTipoDeRutina(request):
    if request.method == "POST":
        nombre = request.POST.get('Nombre')
        descripcion = request.POST.get('Descripcion')
        especialidades_ids = request.POST.getlist('Especialidades')

        tipo = TipoDeRutina.objects.create(
            Nombre=nombre,
            Descripcion=descripcion
        )

        for especialidad_id in especialidades_ids:
            try:
                especialidad_id_int = int(especialidad_id)
                especialidad = Especialidad.objects.get(pk=especialidad_id_int)
                TipoDeRutinaEspecialidad.objects.create(
                    TipoDeRutinaID=tipo,
                    EspecialidadID=especialidad
                )
            except Exception as e:
                print(f"Se produjo un error al procesar la especialidad con ID {especialidad_id}: {e}")


        return redirect('gestionTipoRutinas')

    especialidades = Especialidad.objects.all()
    return render(request, "admin/tipoDeRutina/registrarTipoDeRutina.html", {"especialidades": especialidades})

def editarTipoDeRutina(request, id):
    tipo = get_object_or_404(TipoDeRutina, pk=id)
    if request.method == "POST":
        nombre = request.POST.get('Nombre')
        descripcion = request.POST.get('Descripcion')
        especialidades_ids = request.POST.getlist('Especialidades')
        
        tipo.Nombre = nombre
        tipo.Descripcion = descripcion
        tipo.save()

        TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo).delete()

        for especialidad_id in especialidades_ids:
            try:
                especialidad_id_int = int(especialidad_id)
                especialidad = Especialidad.objects.get(pk=especialidad_id_int)
                TipoDeRutinaEspecialidad.objects.create(
                    TipoDeRutinaID=tipo,
                    EspecialidadID=especialidad
                )
            except Especialidad.DoesNotExist:
                print(f"La especialidad con ID {especialidad_id} no existe.")
        
        return redirect('gestionTipoRutinas')
    
    especialidades = Especialidad.objects.all()
    tipo_especialidades = TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo).select_related('EspecialidadID')
    tipo_especialidades_ids = [especialidad.EspecialidadID.pk for especialidad in tipo_especialidades]

    return render(request, "admin/tipoDeRutina/editarTipoDeRutina.html", {
        "tipo": tipo,
        "especialidades": especialidades,
        "tipo_especialidades_ids": tipo_especialidades_ids
    })

def visualizarTipoDeRutina(request, id):
    tipo = get_object_or_404(TipoDeRutina, pk=id)
    especialidades = TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo).select_related('EspecialidadID')
    
    especialidades_list = [especialidad.EspecialidadID for especialidad in especialidades]
    
    return render(request, "admin/tipoDeRutina/visualizarTipoDeRutina.html", {"tipo": tipo, "especialidades": especialidades_list})

def eliminarTipoDeRutina(request, id):
    tipo = get_object_or_404(TipoDeRutina, pk=id)
    
    rutinas_asociadas = Rutina.objects.filter(TipoID=tipo).exists()
    
    if rutinas_asociadas:
        return render(request, 'admin/error.html', {
            'mensaje': 'No se puede eliminar el tipo de rutina porque está asociado a una o más rutinas.'
        })

    TipoDeRutinaEspecialidad.objects.filter(TipoDeRutinaID=tipo).delete()
    tipo.delete()

    return redirect('gestionTipoRutinas')