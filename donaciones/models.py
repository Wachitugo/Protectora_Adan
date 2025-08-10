from django.db import models

class TipoDonacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_sugerido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='donaciones/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Tipo de donación"
        verbose_name_plural = "Tipos de donaciones"

class Donacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('rechazada', 'Rechazada'),
        ('fallida', 'Fallida'),
    ]
    
    tipo_donacion = models.ForeignKey(TipoDonacion, on_delete=models.CASCADE, related_name='donaciones')
    nombre_donante = models.CharField(max_length=100)
    email_donante = models.EmailField()
    telefono_donante = models.CharField(max_length=20, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    mensaje = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    fecha_donacion = models.DateTimeField(auto_now_add=True)
    anonimo = models.BooleanField(default=False)
    
    # Campos para WebPay
    token_ws = models.CharField(max_length=200, blank=True, null=True, help_text="Token de WebPay")
    buy_order = models.CharField(max_length=100, blank=True, null=True, help_text="Orden de compra")
    session_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID de sesión")
    webpay_response = models.JSONField(blank=True, null=True, help_text="Respuesta completa de WebPay")
    authorization_code = models.CharField(max_length=50, blank=True, null=True, help_text="Código de autorización")
    transaction_date = models.DateTimeField(blank=True, null=True, help_text="Fecha de transacción WebPay")
    
    def __str__(self):
        donante = "Anónimo" if self.anonimo else self.nombre_donante
        return f"Donación de {donante} - ${self.cantidad:,.0f} CLP"
    
    class Meta:
        verbose_name = "Donación"
        verbose_name_plural = "Donaciones"
        ordering = ['-fecha_donacion']

class Aviso(models.Model):
    TIPO_CHOICES = [
        ('urgente', 'Urgente'),
        ('importante', 'Importante'),
        ('informativo', 'Informativo'),
        ('evento', 'Evento'),
    ]
    
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='informativo')
    imagen = models.ImageField(upload_to='avisos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    destacado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Aviso"
        verbose_name_plural = "Avisos"
        ordering = ['-fecha_creacion']
