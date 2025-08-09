from django.db import models

class InformacionAlbergue(models.Model):
    nombre = models.CharField(max_length=200, default="Protectora Adán")
    mision = models.TextField()
    vision = models.TextField()
    historia = models.TextField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    horarios = models.TextField()
    
    # Redes sociales
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    
    # Información adicional
    numero_cuenta = models.CharField(max_length=50, blank=True, help_text="Número de cuenta para donaciones")
    capacidad_perros = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Información del albergue"
        verbose_name_plural = "Información del albergue"

class Voluntario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    experiencia = models.TextField()
    disponibilidad = models.TextField()
    motivacion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
    class Meta:
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"
        ordering = ['-fecha_solicitud']

class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    perro_adoptado = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    mostrar = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Testimonio de {self.nombre}"
    
    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
        ordering = ['-fecha']
