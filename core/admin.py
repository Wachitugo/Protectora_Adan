from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import InformacionAlbergue, Voluntario, Testimonio

@admin.register(InformacionAlbergue)
class InformacionAlbergueAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto_info', 'capacidad_info', 'redes_sociales']
    
    fieldsets = (
        ('🏠 Información Básica', {
            'fields': ('nombre', 'mision', 'vision', 'historia')
        }),
        ('📞 Contacto', {
            'fields': ('direccion', 'telefono', 'email', 'horarios')
        }),
        ('📱 Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'whatsapp')
        }),
        ('📊 Información Adicional', {
            'fields': ('numero_cuenta', 'capacidad_perros')
        }),
    )
    
    def contacto_info(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<div>📞 {}</div>'
            '<div>📧 {}</div>'
            '</div>',
            obj.telefono or 'No definido',
            obj.email or 'No definido'
        )
    contacto_info.short_description = "Contacto"
    
    def capacidad_info(self, obj):
        return format_html(
            '<span style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{} perros</span>',
            obj.capacidad_perros or 'No definida'
        )
    capacidad_info.short_description = "Capacidad"
    
    def redes_sociales(self, obj):
        redes = []
        if obj.facebook_url:
            redes.append("📘 Facebook")
        if obj.instagram_url:
            redes.append("📷 Instagram")
        if obj.twitter_url:
            redes.append("🐦 Twitter")
        if obj.whatsapp:
            redes.append("💬 WhatsApp")
        
        return format_html(
            '<div style="font-size: 12px;">{}</div>',
            '<br>'.join(redes) if redes else 'Sin redes sociales'
        )
    redes_sociales.short_description = "Redes sociales"

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ['voluntario_info', 'contacto', 'direccion', 'fecha_nacimiento', 'experiencia', 'disponibilidad', 'motivacion', 'estado_badges', 'fecha_solicitud']
    list_filter = ['aprobado', 'activo', 'fecha_solicitud']
    search_fields = ['nombre', 'apellidos', 'email', 'telefono']
    readonly_fields = ['fecha_solicitud']
    actions = ['aprobar_voluntarios', 'desactivar_voluntarios', 'activar_voluntarios']
    date_hierarchy = 'fecha_solicitud'
    list_per_page = 25
    
    fieldsets = (
        ('👤 Información Personal', {
            'fields': ('nombre', 'apellidos', 'email', 'telefono', 'direccion', 'fecha_nacimiento')
        }),
        ('💼 Experiencia y Disponibilidad', {
            'fields': ('experiencia', 'disponibilidad')
        }),
        ('📝 Motivación', {
            'fields': ('motivacion',)
        }),
        ('📋 Estado', {
            'fields': ('aprobado', 'activo', 'fecha_solicitud')
        }),
    )
    
    def voluntario_info(self, obj):
        nombre_completo = f"{obj.nombre} {obj.apellidos}"
        return format_html(
            '<div style="font-weight: 500;">{}</div>'
            '<div style="font-size: 12px; color: #6b7280;">{}</div>',
            nombre_completo,
            obj.email
        )
    voluntario_info.short_description = "Voluntario"
    voluntario_info.admin_order_field = 'nombre'
    
    def contacto(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<div>📞 {}</div>'
            '<div>📧 {}</div>'
            '</div>',
            obj.telefono or 'No proporcionado',
            obj.email[:25] + '...' if len(obj.email) > 25 else obj.email
        )
    contacto.short_description = "Contacto"
    
    def estado_badges(self, obj):
        if obj.aprobado:
            estado_aprobacion = '<span style="background: #10b981; color: white; padding: 2px 6px; border-radius: 8px; font-size: 11px; margin-right: 4px;">✅ Aprobado</span>'
        else:
            estado_aprobacion = '<span style="background: #f59e0b; color: white; padding: 2px 6px; border-radius: 8px; font-size: 11px; margin-right: 4px;">⏳ Pendiente</span>'
        
        if obj.activo:
            estado_actividad = '<span style="background: #3b82f6; color: white; padding: 2px 6px; border-radius: 8px; font-size: 11px;">🔵 Activo</span>'
        else:
            estado_actividad = '<span style="background: #6b7280; color: white; padding: 2px 6px; border-radius: 8px; font-size: 11px;">⚫ Inactivo</span>'
        
        return mark_safe(
            f'<div style="display: flex; flex-direction: column; gap: 2px;">{estado_aprobacion}{estado_actividad}</div>'
        )
    estado_badges.short_description = "Estado"
    
    def aprobar_voluntarios(self, request, queryset):
        updated = queryset.update(aprobado=True)
        self.message_user(request, f'✅ {updated} voluntario(s) aprobado(s).')
    aprobar_voluntarios.short_description = "✅ Aprobar voluntarios"
    
    def desactivar_voluntarios(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'❌ {updated} voluntario(s) desactivado(s).')
    desactivar_voluntarios.short_description = "❌ Desactivar voluntarios"
    
    def activar_voluntarios(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'🔵 {updated} voluntario(s) activado(s).')
    activar_voluntarios.short_description = "🔵 Activar voluntarios"

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['testimonio_info', 'imagen_preview', 'estado_badge', 'fecha']
    list_filter = ['mostrar', 'fecha']
    search_fields = ['nombre', 'perro_adoptado', 'contenido']
    readonly_fields = ['fecha', 'imagen_preview']
    actions = ['mostrar_testimonios', 'ocultar_testimonios']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('👤 Información del Testimonio', {
            'fields': ('nombre', 'perro_adoptado', 'contenido', 'imagen', 'imagen_preview')
        }),
        ('📋 Estado', {
            'fields': ('mostrar', 'fecha')
        }),
    )
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"
    
    def testimonio_info(self, obj):
        return format_html(
            '<div style="font-weight: 500;">{}</div>'
            '<div style="font-size: 12px; color: #6b7280;">Perro: {}</div>'
            '<div style="font-size: 12px; color: #6b7280; margin-top: 4px;">{}</div>',
            obj.nombre,
            obj.perro_adoptado or 'No especificado',
            obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
        )
    testimonio_info.short_description = "Testimonio"
    testimonio_info.admin_order_field = 'nombre'
    
    def estado_badge(self, obj):
        if obj.mostrar:
            return format_html(
                '<span style="background: #10b981; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">👁️ Visible</span>'
            )
        else:
            return format_html(
                '<span style="background: #6b7280; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">🙈 Oculto</span>'
            )
    estado_badge.short_description = "Visibilidad"
    estado_badge.admin_order_field = 'mostrar'
    
    def mostrar_testimonios(self, request, queryset):
        updated = queryset.update(mostrar=True)
        self.message_user(request, f'👁️ {updated} testimonio(s) ahora visible(s).')
    mostrar_testimonios.short_description = "👁️ Mostrar testimonios"
    
    def ocultar_testimonios(self, request, queryset):
        updated = queryset.update(mostrar=False)
        self.message_user(request, f'🙈 {updated} testimonio(s) ahora oculto(s).')
    ocultar_testimonios.short_description = "🙈 Ocultar testimonios"
