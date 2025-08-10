from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db.models import Count
from .models import Perro, SolicitudAdopcion, FiltroAdopcion

@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    list_display = ['imagen_preview', 'nombre', 'edad_display', 'caracteristicas', 'estado_badge', 'salud_status', 'solicitudes_count', 'fecha_ingreso']
    list_filter = ['estado', 'tamano', 'sexo', 'color', 'vacunado', 'esterilizado', 'fecha_ingreso']
    search_fields = ['nombre', 'raza', 'descripcion']
    readonly_fields = ['fecha_ingreso', 'imagen_preview', 'solicitudes_count']
    actions = ['marcar_disponible', 'marcar_adoptado', 'marcar_en_proceso']
    list_per_page = 20
    date_hierarchy = 'fecha_ingreso'
    
    fieldsets = (
        ('🐕 Información Básica', {
            'fields': ('nombre', 'edad', 'raza', 'descripcion', 'imagen', 'imagen_preview')
        }),
        ('📏 Características Físicas', {
            'fields': ('tamano', 'sexo', 'color', 'peso')
        }),
        ('🏥 Estado de Salud', {
            'fields': ('vacunado', 'esterilizado', 'necesidades_especiales'),
            'classes': ('collapse',)
        }),
        ('🎾 Comportamiento', {
            'fields': ('bueno_con_niños', 'bueno_con_otros_perros'),
            'classes': ('collapse',)
        }),
        ('📋 Estado y Fechas', {
            'fields': ('estado', 'fecha_ingreso', 'solicitudes_count')
        }),
    )
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"
    
    def edad_display(self, obj):
        return f"{obj.edad} años"
    edad_display.short_description = "Edad"
    edad_display.admin_order_field = 'edad'
    
    def caracteristicas(self, obj):
        return format_html(
            '<span style="background: #e5e7eb; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 4px;">{}</span>'
            '<span style="background: #ddd6fe; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-right: 4px;">{}</span>'
            '<span style="background: #fef3c7; padding: 2px 6px; border-radius: 4px; font-size: 12px;">{}</span>',
            obj.get_tamano_display(),
            obj.get_sexo_display(),
            obj.color
        )
    caracteristicas.short_description = "Características"
    
    def estado_badge(self, obj):
        colors = {
            'disponible': '#10b981',
            'adoptado': '#3b82f6', 
            'en_proceso': '#f59e0b',
            'reservado': '#8b5cf6'
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = 'estado'
    
    def salud_status(self, obj):
        vacuna_icon = "✅" if obj.vacunado else "❌"
        esteril_icon = "✅" if obj.esterilizado else "❌"
        return format_html(
            '<div style="font-size: 12px;">'
            '<div>Vacunado: {}</div>'
            '<div>Esterilizado: {}</div>'
            '</div>',
            vacuna_icon,
            esteril_icon
        )
    salud_status.short_description = "Salud"
    
    def solicitudes_count(self, obj):
        count = obj.solicitudes.count()
        if count > 0:
            url = reverse('admin:adopciones_solicitudadopcion_changelist') + f'?perro__id__exact={obj.id}'
            return format_html(
                '<a href="{}" style="color: #3b82f6; text-decoration: none; font-weight: 500;">{} solicitud{}</a>',
                url,
                count,
                'es' if count != 1 else ''
            )
        return "0 solicitudes"
    solicitudes_count.short_description = "Solicitudes"
    
    def marcar_disponible(self, request, queryset):
        updated = queryset.update(estado='disponible')
        self.message_user(request, f'✅ {updated} perro(s) marcado(s) como disponible(s).')
    marcar_disponible.short_description = "✅ Marcar como disponible"
    
    def marcar_adoptado(self, request, queryset):
        updated = queryset.update(estado='adoptado')
        self.message_user(request, f'🎉 {updated} perro(s) marcado(s) como adoptado(s).')
    marcar_adoptado.short_description = "🎉 Marcar como adoptado"
    
    def marcar_en_proceso(self, request, queryset):
        updated = queryset.update(estado='en_proceso')
        self.message_user(request, f'⏳ {updated} perro(s) marcado(s) como en proceso.')
    marcar_en_proceso.short_description = "⏳ Marcar como en proceso"

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ['solicitante_info', 'perro_link', 'contacto', 'vivienda_info', 'estado_badge', 'fecha_solicitud']
    list_filter = ['estado', 'fecha_solicitud', 'patio', 'otros_animales']
    search_fields = ['nombre_solicitante', 'email', 'perro__nombre', 'telefono']
    readonly_fields = ['fecha_solicitud']
    actions = ['aprobar_solicitudes', 'rechazar_solicitudes', 'marcar_en_revision']
    list_per_page = 25
    date_hierarchy = 'fecha_solicitud'
    
    fieldsets = (
        ('👤 Información del Solicitante', {
            'fields': ('nombre_solicitante', 'email', 'telefono', 'direccion')
        }),
        ('🏠 Información de la Vivienda', {
            'fields': ('vivienda_tipo', 'patio', 'otros_animales')
        }),
        ('🐕 Experiencia y Motivación', {
            'fields': ('experiencia_mascotas', 'motivo_adopcion')
        }),
        ('📋 Estado de la Solicitud', {
            'fields': ('perro', 'estado', 'fecha_solicitud', 'notas_admin'),
            'classes': ('wide',)
        }),
    )
    
    def solicitante_info(self, obj):
        return format_html(
            '<div style="font-weight: 500;">{}</div>'
            '<div style="font-size: 12px; color: #6b7280;">{}</div>',
            obj.nombre_solicitante,
            obj.email
        )
    solicitante_info.short_description = "Solicitante"
    solicitante_info.admin_order_field = 'nombre_solicitante'
    
    def perro_link(self, obj):
        url = reverse('admin:adopciones_perro_change', args=[obj.perro.id])
        return format_html(
            '<a href="{}" style="color: #3b82f6; text-decoration: none; font-weight: 500;">{}</a>',
            url,
            obj.perro.nombre
        )
    perro_link.short_description = "Perro"
    perro_link.admin_order_field = 'perro__nombre'
    
    def contacto(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<div>📞 {}</div>'
            '<div>📧 {}</div>'
            '</div>',
            obj.telefono,
            obj.email[:25] + '...' if len(obj.email) > 25 else obj.email
        )
    contacto.short_description = "Contacto"
    
    def vivienda_info(self, obj):
        patio_icon = "🏡" if obj.patio else "🏢"
        # Usar try/except para compatibilidad con datos existentes
        try:
            vivienda_display = obj.get_vivienda_tipo_display()
        except:
            vivienda_display = obj.vivienda_tipo
        
        return format_html(
            '<div style="font-size: 12px;">'
            '<div>{} {}</div>'
            '<div>Otros animales: {}</div>'
            '</div>',
            patio_icon,
            vivienda_display,
            "Sí" if obj.otros_animales else "No"
        )
    vivienda_info.short_description = "Vivienda"
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#f59e0b',
            'en_revision': '#3b82f6',
            'aprobada': '#10b981',
            'rechazada': '#ef4444'
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = 'estado'
    
    def aprobar_solicitudes(self, request, queryset):
        updated = queryset.update(estado='aprobada')
        self.message_user(request, f'✅ {updated} solicitud(es) aprobada(s).')
    aprobar_solicitudes.short_description = "✅ Aprobar solicitudes"
    
    def rechazar_solicitudes(self, request, queryset):
        updated = queryset.update(estado='rechazada')
        self.message_user(request, f'❌ {updated} solicitud(es) rechazada(s).')
    rechazar_solicitudes.short_description = "❌ Rechazar solicitudes"
    
    def marcar_en_revision(self, request, queryset):
        updated = queryset.update(estado='en_revision')
        self.message_user(request, f'🔍 {updated} solicitud(es) marcada(s) como en revisión.')
    marcar_en_revision.short_description = "🔍 Marcar en revisión"

@admin.register(FiltroAdopcion)
class FiltroAdopcionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'filtros_aplicados', 'created_at']
    list_filter = ['tamano', 'sexo', 'color', 'created_at']
    readonly_fields = ['created_at']
    
    def filtros_aplicados(self, obj):
        filtros = []
        if obj.tamano:
            filtros.append(f"Tamaño: {obj.get_tamano_display()}")
        if obj.sexo:
            filtros.append(f"Sexo: {obj.get_sexo_display()}")
        if obj.color:
            filtros.append(f"Color: {obj.color}")
        
        return format_html(
            '<div style="font-size: 12px;">{}</div>',
            '<br>'.join(filtros) if filtros else 'Sin filtros'
        )
    filtros_aplicados.short_description = "Filtros aplicados"
