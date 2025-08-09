from django.contrib import admin
from .models import InformacionAlbergue, Voluntario, Testimonio

@admin.register(InformacionAlbergue)
class InformacionAlbergueAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'mision', 'vision', 'historia')
        }),
        ('Contacto', {
            'fields': ('direccion', 'telefono', 'email', 'horarios')
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'whatsapp')
        }),
        ('Información Adicional', {
            'fields': ('numero_cuenta', 'capacidad_perros')
        }),
    )

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'email', 'telefono', 'fecha_solicitud', 'aprobado', 'activo']
    list_filter = ['aprobado', 'activo', 'fecha_solicitud']
    search_fields = ['nombre', 'apellidos', 'email']
    readonly_fields = ['fecha_solicitud']
    actions = ['aprobar_voluntarios', 'desactivar_voluntarios']
    
    def aprobar_voluntarios(self, request, queryset):
        queryset.update(aprobado=True)
        self.message_user(request, f'{queryset.count()} voluntarios aprobados.')
    aprobar_voluntarios.short_description = "Aprobar voluntarios seleccionados"
    
    def desactivar_voluntarios(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, f'{queryset.count()} voluntarios desactivados.')
    desactivar_voluntarios.short_description = "Desactivar voluntarios seleccionados"

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'perro_adoptado', 'fecha', 'mostrar']
    list_filter = ['mostrar', 'fecha']
    search_fields = ['nombre', 'perro_adoptado']
    readonly_fields = ['fecha']
