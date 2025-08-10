from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from django.urls import reverse
from datetime import datetime, timedelta
from .models import TipoDonacion, Donacion, Aviso

@admin.register(TipoDonacion)
class TipoDonacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_formateado', 'estado_badge', 'donaciones_count', 'total_recaudado']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    actions = ['activar_tipos', 'desactivar_tipos']
    
    def precio_formateado(self, obj):
        return format_html(
            '<span style="font-weight: 500; color: #059669;">${} CLP</span>',
            f"{obj.precio_sugerido:,.0f}"
        )
    precio_formateado.short_description = "Precio sugerido"
    precio_formateado.admin_order_field = 'precio_sugerido'
    
    def estado_badge(self, obj):
        color = '#10b981' if obj.activo else '#ef4444'
        texto = 'Activo' if obj.activo else 'Inactivo'
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, texto
        )
    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = 'activo'
    
    def donaciones_count(self, obj):
        count = obj.donaciones.filter(estado='completada').count()
        return format_html(
            '<span style="font-weight: 500;">{} donacion{}</span>',
            count, 'es' if count != 1 else ''
        )
    donaciones_count.short_description = "Donaciones"
    
    def total_recaudado(self, obj):
        total = obj.donaciones.filter(estado='completada').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        return format_html(
            '<span style="font-weight: 500; color: #059669;">${}</span>',
            f"{total:,.0f}"
        )
    total_recaudado.short_description = "Total recaudado"
    
    def activar_tipos(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'✅ {updated} tipo(s) de donación activado(s).')
    activar_tipos.short_description = "✅ Activar tipos seleccionados"
    
    def desactivar_tipos(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'❌ {updated} tipo(s) de donación desactivado(s).')
    desactivar_tipos.short_description = "❌ Desactivar tipos seleccionados"

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ['donante_info', 'tipo_donacion', 'cantidad_formateada', 'estado_badge', 'pago_info', 'fecha_donacion']
    list_filter = ['estado', 'anonimo', 'fecha_donacion', 'tipo_donacion']
    search_fields = ['nombre_donante', 'email_donante', 'buy_order']
    readonly_fields = ['fecha_donacion', 'buy_order', 'authorization_code']
    actions = ['marcar_completada', 'marcar_cancelada', 'marcar_fallida']
    list_per_page = 25
    date_hierarchy = 'fecha_donacion'
    
    fieldsets = (
        ('👤 Información del Donante', {
            'fields': ('nombre_donante', 'email_donante', 'telefono_donante', 'anonimo')
        }),
        ('💰 Información de la Donación', {
            'fields': ('tipo_donacion', 'cantidad', 'mensaje')
        }),
        ('💳 Información de Pago', {
            'fields': ('buy_order', 'authorization_code'),
            'classes': ('collapse',)
        }),
        ('📋 Estado', {
            'fields': ('estado', 'fecha_donacion')
        }),
    )
    
    def donante_info(self, obj):
        nombre = obj.nombre_donante if not obj.anonimo else "Anónimo"
        icono = "🕶️" if obj.anonimo else "👤"
        return format_html(
            '<div style="font-weight: 500;">{} {}</div>'
            '<div style="font-size: 12px; color: #6b7280;">{}</div>',
            icono, nombre, obj.email_donante
        )
    donante_info.short_description = "Donante"
    donante_info.admin_order_field = 'nombre_donante'
    
    def cantidad_formateada(self, obj):
        return format_html(
            '<div><span style="font-weight: 600; color: #059669; font-size: 16px;">${}</span></div>'
            '<div style="font-size: 12px; color: #6b7280;">CLP</div>',
            f"{obj.cantidad:,.0f}"
        )
    cantidad_formateada.short_description = "Cantidad"
    cantidad_formateada.admin_order_field = 'cantidad'
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#f59e0b',
            'completada': '#10b981',
            'fallida': '#ef4444',
            'cancelada': '#6b7280'
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = 'estado'
    
    def pago_info(self, obj):
        if obj.buy_order:
            return format_html(
                '<div style="font-size: 12px;">'
                '<div><strong>Orden:</strong> {}</div>'
                '<div><strong>Auth:</strong> {}</div>'
                '</div>',
                obj.buy_order[:15] + '...' if len(obj.buy_order) > 15 else obj.buy_order,
                obj.authorization_code or 'N/A'
            )
        return "Sin información de pago"
    pago_info.short_description = "Info. Pago"
    
    def marcar_completada(self, request, queryset):
        updated = queryset.update(estado='completada')
        self.message_user(request, f'✅ {updated} donación(es) marcada(s) como completada(s).')
    marcar_completada.short_description = "✅ Marcar como completada"
    
    def marcar_cancelada(self, request, queryset):
        updated = queryset.update(estado='cancelada')
        self.message_user(request, f'❌ {updated} donación(es) cancelada(s).')
    marcar_cancelada.short_description = "❌ Marcar como cancelada"
    
    def marcar_fallida(self, request, queryset):
        updated = queryset.update(estado='fallida')
        self.message_user(request, f'⚠️ {updated} donación(es) marcada(s) como fallida(s).')
    marcar_fallida.short_description = "⚠️ Marcar como fallida"

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo_badge', 'estado_badge', 'destacado_badge', 'fecha_info', 'imagen_preview']
    list_filter = ['tipo', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['titulo', 'contenido']
    readonly_fields = ['fecha_creacion', 'imagen_preview']
    actions = ['activar_avisos', 'desactivar_avisos', 'destacar_avisos']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('📢 Información del Aviso', {
            'fields': ('titulo', 'contenido', 'imagen', 'imagen_preview')
        }),
        ('⚙️ Configuración', {
            'fields': ('tipo', 'activo', 'destacado', 'fecha_vencimiento')
        }),
        ('📅 Fechas', {
            'fields': ('fecha_creacion',)
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
    
    def tipo_badge(self, obj):
        colors = {
            'urgente': '#ef4444',
            'necesidad': '#f59e0b',
            'evento': '#3b82f6',
            'noticia': '#10b981'
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = "Tipo"
    tipo_badge.admin_order_field = 'tipo'
    
    def estado_badge(self, obj):
        color = '#10b981' if obj.activo else '#ef4444'
        texto = 'Activo' if obj.activo else 'Inactivo'
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, texto
        )
    estado_badge.short_description = "Estado"
    estado_badge.admin_order_field = 'activo'
    
    def destacado_badge(self, obj):
        if obj.destacado:
            return format_html(
                '<span style="background: #8b5cf6; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 500;">⭐ Destacado</span>'
            )
        return ""
    destacado_badge.short_description = "Destacado"
    destacado_badge.admin_order_field = 'destacado'
    
    def fecha_info(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<div><strong>Creado:</strong> {}</div>'
            '<div><strong>Vence:</strong> {}</div>'
            '</div>',
            obj.fecha_creacion.strftime("%d/%m/%Y"),
            obj.fecha_vencimiento.strftime("%d/%m/%Y") if obj.fecha_vencimiento else "Sin vencimiento"
        )
    fecha_info.short_description = "Fechas"
    
    def activar_avisos(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'✅ {updated} aviso(s) activado(s).')
    activar_avisos.short_description = "✅ Activar avisos"
    
    def desactivar_avisos(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'❌ {updated} aviso(s) desactivado(s).')
    desactivar_avisos.short_description = "❌ Desactivar avisos"
    
    def destacar_avisos(self, request, queryset):
        updated = queryset.update(destacado=True)
        self.message_user(request, f'⭐ {updated} aviso(s) destacado(s).')
    destacar_avisos.short_description = "⭐ Destacar avisos"
