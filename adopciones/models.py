from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

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
    
    VIVIENDA_TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('duplex', 'Dúplex'),
        ('parcela', 'Parcela'),
        ('otro', 'Otro'),
    ]
    
    PATIO_CHOICES = [
        ('si', 'Sí, tengo patio'),
        ('no', 'No tengo patio'),
        ('pequeño', 'Tengo un patio pequeño'),
        ('grande', 'Tengo un patio grande'),
    ]
    
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name='solicitudes')
    nombre_solicitante = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    experiencia_mascotas = models.TextField()
    motivo_adopcion = models.TextField()
    vivienda_tipo = models.CharField(max_length=20, choices=VIVIENDA_TIPO_CHOICES)
    patio = models.CharField(max_length=20, choices=PATIO_CHOICES)
    otros_animales = models.TextField(blank=True, help_text="Describe otros animales en casa")
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


# Señales para actualizar automáticamente el estado del perro
@receiver(post_save, sender=SolicitudAdopcion)
def actualizar_estado_perro(sender, instance, created, **kwargs):
    """
    Actualiza automáticamente el estado del perro cuando se aprueba una solicitud de adopción
    """
    if instance.estado == 'aprobada':
        # Marcar el perro como adoptado
        perro = instance.perro
        if perro.estado != 'adoptado':
            perro.estado = 'adoptado'
            perro.save()
            
        # Rechazar automáticamente otras solicitudes pendientes para el mismo perro
        otras_solicitudes = SolicitudAdopcion.objects.filter(
            perro=perro,
            estado__in=['pendiente', 'en_revision']
        ).exclude(id=instance.id)
        
        if otras_solicitudes.exists():
            otras_solicitudes.update(estado='rechazada')
    
    elif instance.estado in ['pendiente', 'en_revision']:
        # Si la solicitud vuelve a pendiente o revisión, marcar perro como en proceso
        perro = instance.perro
        if perro.estado == 'disponible':
            perro.estado = 'en_proceso'
            perro.save()
    
    elif instance.estado == 'rechazada':
        # Si se rechaza esta solicitud, verificar si hay otras solicitudes activas
        perro = instance.perro
        solicitudes_activas = SolicitudAdopcion.objects.filter(
            perro=perro,
            estado__in=['pendiente', 'en_revision', 'aprobada']
        ).exclude(id=instance.id)
        
        # Si no hay otras solicitudes activas, marcar perro como disponible
        if not solicitudes_activas.exists():
            perro.estado = 'disponible'
            perro.save()
