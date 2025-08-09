from django.contrib import admin
from .models import Perro, SolicitudAdopcion, FiltroAdopcion

@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edad', 'tamano', 'sexo', 'color', 'estado', 'fecha_ingreso']
    list_filter = ['estado', 'tamano', 'sexo', 'color', 'vacunado', 'esterilizado', 'fecha_ingreso']
    search_fields = ['nombre', 'raza', 'descripcion']
    readonly_fields = ['fecha_ingreso']
    actions = ['marcar_disponible', 'marcar_adoptado']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'edad', 'raza', 'descripcion', 'imagen')
        }),
        ('Características', {
            'fields': ('tamano', 'sexo', 'color', 'peso')
        }),
        ('Estado de Salud', {
            'fields': ('vacunado', 'esterilizado', 'necesidades_especiales')
        }),
        ('Comportamiento', {
            'fields': ('bueno_con_niños', 'bueno_con_otros_perros')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_ingreso')
        }),
    )
    
    def marcar_disponible(self, request, queryset):
        queryset.update(estado='disponible')
        self.message_user(request, f'{queryset.count()} perros marcados como disponibles.')
    marcar_disponible.short_description = "Marcar como disponible"
    
    def marcar_adoptado(self, request, queryset):
        queryset.update(estado='adoptado')
        self.message_user(request, f'{queryset.count()} perros marcados como adoptados.')
    marcar_adoptado.short_description = "Marcar como adoptado"

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ['nombre_solicitante', 'perro', 'email', 'telefono', 'estado', 'fecha_solicitud']
    list_filter = ['estado', 'fecha_solicitud', 'patio']
    search_fields = ['nombre_solicitante', 'email', 'perro__nombre']
    readonly_fields = ['fecha_solicitud']
    actions = ['aprobar_solicitudes', 'rechazar_solicitudes']
    
    fieldsets = (
        ('Información del Solicitante', {
            'fields': ('nombre_solicitante', 'email', 'telefono', 'direccion')
        }),
        ('Información de la Vivienda', {
            'fields': ('vivienda_tipo', 'patio', 'otros_animales')
        }),
        ('Experiencia y Motivación', {
            'fields': ('experiencia_mascotas', 'motivo_adopcion')
        }),
        ('Estado de la Solicitud', {
            'fields': ('perro', 'estado', 'fecha_solicitud', 'notas_admin')
        }),
    )
    
    def aprobar_solicitudes(self, request, queryset):
        queryset.update(estado='aprobada')
        self.message_user(request, f'{queryset.count()} solicitudes aprobadas.')
    aprobar_solicitudes.short_description = "Aprobar solicitudes seleccionadas"
    
    def rechazar_solicitudes(self, request, queryset):
        queryset.update(estado='rechazada')
        self.message_user(request, f'{queryset.count()} solicitudes rechazadas.')
    rechazar_solicitudes.short_description = "Rechazar solicitudes seleccionadas"

@admin.register(FiltroAdopcion)
class FiltroAdopcionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'tamano', 'sexo', 'color', 'created_at']
    list_filter = ['tamano', 'sexo', 'color', 'created_at']
    readonly_fields = ['created_at']
