from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q, Sum
from .models import InformacionAlbergue, Voluntario, Testimonio
from adopciones.models import Perro
from donaciones.models import Aviso, Donacion
from .forms import VoluntarioForm

def home(request):
    """Vista principal del sitio"""
    # Obtener perros destacados (disponibles)
    perros_destacados = Perro.objects.filter(estado='disponible')[:3]
    
    # Obtener avisos activos
    avisos = Aviso.objects.filter(activo=True)[:3]
    
    # Obtener testimonios
    testimonios = Testimonio.objects.filter(mostrar=True)[:4]
    
    # Estadísticas
    stats = {
        'adoptados': Perro.objects.filter(estado='adoptado').count(),
        'disponibles': Perro.objects.filter(estado='disponible').count(),
        'voluntarios': Voluntario.objects.filter(activo=True).count(),
        'donaciones': Donacion.objects.filter(estado='completada').aggregate(
            total=Sum('cantidad')
        )['total'] or 0
    }
    
    context = {
        'perros_destacados': perros_destacados,
        'avisos': avisos,
        'testimonios': testimonios,
        'stats': stats,
    }
    
    return render(request, 'home.html', context)

def about(request):
    """Vista sobre nosotros"""
    try:
        info_albergue = InformacionAlbergue.objects.first()
    except InformacionAlbergue.DoesNotExist:
        info_albergue = None
    
    context = {
        'info_albergue': info_albergue,
    }
    
    return render(request, 'core/about.html', context)

def voluntariado(request):
    """Vista para el formulario de voluntariado"""
    if request.method == 'POST':
        print(f"=== POST REQUEST RECEIVED ===")
        print(f"POST data: {dict(request.POST)}")
        form = VoluntarioForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            print(f"SUCCESS: Volunteer saved with ID {volunteer.id}")
            messages.success(request, '¡Gracias por tu interés! Hemos recibido tu solicitud de voluntariado.')
            return redirect('core:voluntariado')
        else:
            print(f"FORM ERRORS: {form.errors}")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = VoluntarioForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'core/voluntariado.html', context)
