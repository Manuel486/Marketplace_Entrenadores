from django.db import models
from django.utils import timezone

class TipoDeRutina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Local(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Instructor(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    especialidad = models.CharField(max_length=100)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, default=1)  # Relación con Local

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.especialidad} ({self.local})"

class Frecuencia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return f"{self.nombre} - {self.instructor.nombres} {self.instructor.apellidos}"

class Cliente(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE)
    talla = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentaje_grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nivel_condicion_fisica = models.CharField(max_length=50, null=True, blank=True)
    objetivo_principal = models.CharField(max_length=255, null=True, blank=True)
    historial_lesiones = models.TextField(null=True, blank=True)
    enfermedades_preexistentes = models.TextField(null=True, blank=True)
    preferencias_entrenamiento = models.TextField(null=True, blank=True)
    disponibilidad_horaria = models.CharField(max_length=100, null=True, blank=True)
    fecha_registro = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido}"

class Rutina(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(TipoDeRutina, on_delete=models.CASCADE)
    descripcion = models.TextField()
    frecuencia = models.ForeignKey(Frecuencia, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    horas_recomendadas = models.CharField(max_length=50)
    objetivos = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.nombre} - {self.frecuencia.nombre} ({self.instructor})"

class Dieta(models.Model):
    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.lastname} ({self.username})"