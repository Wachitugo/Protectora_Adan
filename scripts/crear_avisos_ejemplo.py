#!/usr/bin/env python
"""
Script para crear avisos de ejemplo
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protectora_adan.settings')
django.setup()

from donaciones.models import Aviso

def crear_avisos_ejemplo():
    """Crear avisos de ejemplo para mostrar el sistema"""
    
    avisos_ejemplo = [
        {
            'titulo': '🚨 Necesitamos voluntarios urgentemente',
            'contenido': 'Estamos buscando personas comprometidas para ayudar en el cuidado diario de nuestros perros. Solo necesitas 2-3 horas a la semana y muchas ganas de ayudar. ¡Tu tiempo puede cambiar vidas!',
            'tipo': 'urgente',
            'destacado': True,
            'fecha_vencimiento': datetime.now() + timedelta(days=30)
        },
        {
            'titulo': '📅 Jornada de adopción este sábado',
            'contenido': 'Te invitamos a nuestra jornada especial de adopción el sábado 10 de agosto de 10:00 a 16:00. Ven a conocer a nuestros perros y tal vez encuentres a tu nuevo mejor amigo. Habrá actividades para toda la familia.',
            'tipo': 'evento',
            'destacado': True,
            'fecha_vencimiento': datetime.now() + timedelta(days=7)
        },
        {
            'titulo': '💊 Campaña de vacunación gratuita',
            'contenido': 'En alianza con veterinarios locales, ofrecemos vacunación gratuita para perros de la comunidad. Cupos limitados, inscripciones abiertas desde hoy.',
            'tipo': 'importante',
            'destacado': False,
            'fecha_vencimiento': datetime.now() + timedelta(days=15)
        },
        {
            'titulo': '🎉 ¡Celebramos 50 adopciones exitosas!',
            'contenido': 'Estamos muy orgullosos de anunciar que hemos logrado 50 adopciones exitosas en lo que va del año. Gracias a todos los que han hecho esto posible: adoptantes, voluntarios y donantes.',
            'tipo': 'informativo',
            'destacado': False,
            'fecha_vencimiento': None
        }
    ]
    
    print("Creando avisos de ejemplo...")
    
    for aviso_data in avisos_ejemplo:
        aviso, created = Aviso.objects.get_or_create(
            titulo=aviso_data['titulo'],
            defaults=aviso_data
        )
        
        if created:
            print(f"✅ Creado: {aviso.titulo}")
        else:
            print(f"⚠️  Ya existe: {aviso.titulo}")
    
    print(f"\n📊 Total de avisos activos: {Aviso.objects.filter(activo=True).count()}")

if __name__ == "__main__":
    crear_avisos_ejemplo()
