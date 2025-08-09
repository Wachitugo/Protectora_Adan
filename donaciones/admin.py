from django.contrib import admin
from .models import TipoDonacion, Donacion, Aviso

@admin.register(TipoDonacion)
class TipoDonacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_sugerido', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_donante', 'tipo_donacion', 'cantidad', 'estado', 'fecha_donacion', 'anonimo']
    list_filter = ['estado', 'anonimo', 'fecha_donacion', 'tipo_donacion']
    search_fields = ['nombre_donante', 'email_donante']
    readonly_fields = ['fecha_donacion']
    actions = ['marcar_completada', 'marcar_cancelada']
    
    fieldsets = (
        ('Información del Donante', {
            'fields': ('nombre_donante', 'email_donante', 'telefono_donante', 'anonimo')
        }),
        ('Información de la Donación', {
            'fields': ('tipo_donacion', 'cantidad', 'mensaje')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_donacion')
        }),
    )
    
    def marcar_completada(self, request, queryset):
        queryset.update(estado='completada')
        self.message_user(request, f'{queryset.count()} donaciones marcadas como completadas.')
    marcar_completada.short_description = "Marcar como completada"
    
    def marcar_cancelada(self, request, queryset):
        queryset.update(estado='cancelada')
        self.message_user(request, f'{queryset.count()} donaciones canceladas.')
    marcar_cancelada.short_description = "Marcar como cancelada"

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'activo', 'destacado', 'fecha_creacion', 'fecha_vencimiento']
    list_filter = ['tipo', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['titulo', 'contenido']
    readonly_fields = ['fecha_creacion']
    actions = ['activar_avisos', 'desactivar_avisos']
    
    fieldsets = (
        ('Información del Aviso', {
            'fields': ('titulo', 'contenido', 'imagen')
        }),
        ('Configuración', {
            'fields': ('tipo', 'activo', 'destacado', 'fecha_vencimiento')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',)
        }),
    )
    
    def activar_avisos(self, request, queryset):
        queryset.update(activo=True)
        self.message_user(request, f'{queryset.count()} avisos activados.')
    activar_avisos.short_description = "Activar avisos seleccionados"
    
    def desactivar_avisos(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, f'{queryset.count()} avisos desactivados.')
    desactivar_avisos.short_description = "Desactivar avisos seleccionados"
