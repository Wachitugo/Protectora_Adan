from django.db import models
from django.contrib.auth.models import User

class Perro(models.Model):
    TAMANO_CHOICES = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    COLOR_CHOICES = [
        ('negro', 'Negro'),
        ('blanco', 'Blanco'),
        ('marron', 'Marrón'),
        ('dorado', 'Dorado'),
        ('gris', 'Gris'),
        ('mixto', 'Mixto'),
    ]
    
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En proceso de adopción'),
        ('adoptado', 'Adoptado'),
    ]
    
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(help_text="Edad en años")
    tamano = models.CharField(max_length=10, choices=TAMANO_CHOICES)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    raza = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='perros/', blank=True, null=True)
    vacunado = models.BooleanField(default=False)
    esterilizado = models.BooleanField(default=False)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='disponible')
    fecha_ingreso = models.DateField(auto_now_add=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Peso en kg")
    bueno_con_niños = models.BooleanField(default=True)
    bueno_con_otros_perros = models.BooleanField(default=True)
    necesidades_especiales = models.TextField(blank=True, help_text="Descripción de necesidades especiales")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Perro"
        verbose_name_plural = "Perros"
        ordering = ['-fecha_ingreso']

class SolicitudAdopcion(models.Model):
    ESTADO_SOLICITUD_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE)
    nombre_solicitante = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    experiencia_mascotas = models.TextField()
    motivo_adopcion = models.TextField()
    vivienda_tipo = models.CharField(max_length=100)
    patio = models.BooleanField(default=False)
    otros_animales = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_SOLICITUD_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    notas_admin = models.TextField(blank=True)
    
    def __str__(self):
        return f"Solicitud de {self.nombre_solicitante} para {self.perro.nombre}"
    
    class Meta:
        verbose_name = "Solicitud de adopción"
        verbose_name_plural = "Solicitudes de adopción"
        ordering = ['-fecha_solicitud']

class FiltroAdopcion(models.Model):
    """Modelo para almacenar filtros de búsqueda de usuarios"""
    session_key = models.CharField(max_length=40)
    tamano = models.CharField(max_length=10, choices=Perro.TAMANO_CHOICES, blank=True)
    sexo = models.CharField(max_length=10, choices=Perro.SEXO_CHOICES, blank=True)
    color = models.CharField(max_length=10, choices=Perro.COLOR_CHOICES, blank=True)
    edad_min = models.PositiveIntegerField(null=True, blank=True)
    edad_max = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Filtro de adopción"
        verbose_name_plural = "Filtros de adopción"
