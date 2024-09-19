from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class Especialidad(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    EspecialidadID = models.AutoField(primary_key=True, db_column='EspecialidadID')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo', db_column='Estado')
    FechaCreacion = models.DateField(default=timezone.now, db_column='FechaCreacion')
    FechaActualizacion = models.DateField(auto_now=True, db_column='FechaActualizacion')

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'Especialidad'

class TipoDeRutina(models.Model):
    TipoDeRutinaID = models.AutoField(primary_key=True, db_column='TipoDeRutinaID')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Descripcion = models.TextField(blank=True, null=True, db_column='Descripcion')

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'TipoDeRutina'

class TipoDeRutinaEspecialidad(models.Model):
    TipoDeRutinaEspecialidadID = models.AutoField(primary_key=True, db_column='TipoDeRutinaEspecialidadID')
    TipoDeRutinaID = models.ForeignKey(TipoDeRutina, on_delete=models.CASCADE, db_column='TipoDeRutinaID')
    EspecialidadID = models.ForeignKey(Especialidad, on_delete=models.CASCADE, db_column='EspecialidadID')

    class Meta:
        db_table = 'TipoDeRutinaEspecialidad'
        unique_together = ('TipoDeRutinaID', 'EspecialidadID')

class MetaPredeterminada(models.Model):
    MetaPredeterminadaID = models.AutoField(primary_key=True, db_column='MetaPredeterminadaID')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    TipoDeRutinaID = models.ForeignKey(TipoDeRutina, on_delete=models.CASCADE, db_column='TipoDeRutinaID')

    def __str__(self):
            return self.Nombre
    
    class Meta:
        db_table = 'MetaPredeterminada'

class Local(models.Model):
    LocalID = models.AutoField(primary_key=True, db_column='LocalID')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Direccion = models.CharField(max_length=255, db_column='Direccion')
    Telefono = models.CharField(max_length=20, blank=True, null=True, db_column='Telefono')

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'Local'

class Instructor(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    InstructorID = models.AutoField(primary_key=True, db_column='InstructorID')
    UsuarioID = models.OneToOneField('Usuario', on_delete=models.CASCADE, db_column='UsuarioID')
    Nombres = models.CharField(max_length=100, db_column='Nombres')
    Apellidos = models.CharField(max_length=100, db_column='Apellidos')
    Email = models.EmailField(max_length=100, db_column='Email')
    Edad = models.IntegerField(db_column='Edad')
    Sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, db_column='Sexo')
    FechaNacimiento = models.DateField(db_column='FechaNacimiento')
    Especialidad = models.ManyToManyField(Especialidad, through='EspecialidadInstructor', related_name='instructores', db_column='EspecialidadID')
    Local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True, db_column='LocalID')

    def __str__(self):
        return f"{self.Nombres} {self.Apellidos}"

    class Meta:
        db_table = 'Instructor'

class Horario(models.Model):
    DIA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    HorarioID = models.AutoField(primary_key=True, db_column='HorarioID')
    Dia = models.CharField(max_length=10, choices=DIA_CHOICES, db_column='Dia')
    HoraInicio = models.TimeField(db_column='HoraInicio')
    HoraFin = models.TimeField(db_column='HoraFin')
    InstructorID = models.ForeignKey('Instructor', on_delete=models.CASCADE, db_column='InstructorID')

    def __str__(self):
        return f"{self.Dia} ({self.HoraInicio} - {self.HoraFin})"

    class Meta:
        db_table = 'Horario'


class EspecialidadInstructor(models.Model):
    EspecialidadInstructorID = models.AutoField(primary_key=True, db_column='EspecialidadInstructorID')
    InstructorID = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='InstructorID')
    EspecialidadID = models.ForeignKey(Especialidad, on_delete=models.CASCADE, db_column='EspecialidadID')

    class Meta:
        db_table = 'EspecialidadInstructor'
        unique_together = ('InstructorID', 'EspecialidadID')

class InformacionPersonalInstructor(models.Model):
    InfoPersonalID = models.AutoField(primary_key=True, db_column='InfoPersonalID')
    InstructorID = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='InstructorID')
    PreferenciaHorario = models.CharField(max_length=100, db_column='PreferenciaHorario')

    class Meta:
        db_table = 'InformacionPersonalInstructor'

class Cliente(models.Model):
    ClienteID = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True, db_column='ClienteID')
    Talla = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='Talla')
    PorcentajeGrasaCorporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='PorcentajeGrasaCorporal')
    NivelCondicionFisica = models.CharField(max_length=50, null=True, blank=True, db_column='NivelCondicionFisica')
    ObjetivoPrincipal = models.CharField(max_length=255, null=True, blank=True, db_column='ObjetivoPrincipal')
    HistorialLesiones = models.TextField(null=True, blank=True, db_column='HistorialLesiones')
    EnfermedadesPreexistentes = models.TextField(null=True, blank=True, db_column='EnfermedadesPreexistentes')
    PreferenciasEntrenamiento = models.TextField(null=True, blank=True, db_column='PreferenciasEntrenamiento')
    FechaRegistro = models.DateField(default=timezone.now, db_column='FechaRegistro')

    def __str__(self):
        return f"{self.ClienteID.Nombre} {self.ClienteID.Apellido}"

    class Meta:
        db_table = 'Cliente'

class Rutina(models.Model):
    RutinaID = models.AutoField(primary_key=True, db_column='RutinaID')
    Nombre = models.CharField(max_length=255, db_column='Nombre')
    TipoID = models.ForeignKey(TipoDeRutina, on_delete=models.CASCADE, db_column='TipoID')
    Descripcion = models.TextField(null=True, db_column='Descripcion')
    Frecuencia = models.TextField(max_length=50, db_column='Frecuencia')
    FechaInicio = models.DateField(db_column='FechaInicio')
    FechaFin = models.DateField(db_column='FechaFin')
    Imagen1 = models.ImageField(upload_to='imagenes/', blank=True, null=True, db_column='Imagen1')
    Imagen2 = models.ImageField(upload_to='imagenes/', blank=True, null=True, db_column='Imagen2')
    InstructorID = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_column='InstructorID')
    ClienteID = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, db_column='ClienteID')
    Objetivos = models.CharField(max_length=255, db_column='Objetivos')

    def __str__(self):
        return f"{self.Nombre} - {self.Frecuencia} ({self.InstructorID})"

    class Meta:
        db_table = 'Rutina'

class Meta(models.Model):
    MetaID = models.AutoField(primary_key=True, db_column='MetaID')
    Nombre = models.CharField(max_length=255, db_column='Nombre')
    EstadoInicial = models.DecimalField(max_digits=5, decimal_places=2, db_column='EstadoInicial')
    EstadoFinal = models.DecimalField(max_digits=5, decimal_places=2, db_column='EstadoFinal')
    RutinaID = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='objetivos', db_column='RutinaID')

    def __str__(self):
        return f"{self.Nombre} (Inicial: {self.EstadoInicial}, Final: {self.EstadoFinal})"

    class Meta:
        db_table = 'Meta'

class Usuario(models.Model):
    TIPO_CHOICES = [
        ('Instructor', 'Instructor'),
        ('Administrador', 'Administrador'),
    ]
    UsuarioID = models.AutoField(primary_key=True, db_column='UsuarioID')
    Username = models.CharField(max_length=100, db_column='Username')
    Password = models.CharField(max_length=100, db_column='Password')
    Email = models.EmailField(max_length=100, db_column='Email')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Apellido = models.CharField(max_length=100, db_column='Apellido')
    Tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, db_column='Tipo')

    def __str__(self):
        return f"{self.Nombre} {self.Apellido} ({self.Username})"

    class Meta:
        db_table = 'Usuario'
