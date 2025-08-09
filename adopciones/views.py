from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Perro, SolicitudAdopcion
from .forms import SolicitudAdopcionForm, FiltroPerrosForm

def lista_perros(request):
    """Vista para mostrar la lista de perros disponibles"""
    form = FiltroPerrosForm(request.GET)
    perros = Perro.objects.filter(estado='disponible')
    
    # Aplicar filtros
    if form.is_valid():
        if form.cleaned_data.get('tamano'):
            perros = perros.filter(tamano=form.cleaned_data['tamano'])
        if form.cleaned_data.get('sexo'):
            perros = perros.filter(sexo=form.cleaned_data['sexo'])
        if form.cleaned_data.get('color'):
            perros = perros.filter(color=form.cleaned_data['color'])
        if form.cleaned_data.get('edad_min'):
            perros = perros.filter(edad__gte=form.cleaned_data['edad_min'])
        if form.cleaned_data.get('edad_max'):
            perros = perros.filter(edad__lte=form.cleaned_data['edad_max'])
    
    # Paginación
    paginator = Paginator(perros, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'perros': page_obj,
        'form': form,
        'total_perros': perros.count(),
    }
    
    return render(request, 'adopciones/lista_perros.html', context)

def detalle_perro(request, perro_id):
    """Vista para mostrar los detalles de un perro específico"""
    perro = get_object_or_404(Perro, id=perro_id)
    
    context = {
        'perro': perro,
    }
    
    return render(request, 'adopciones/detalle_perro.html', context)

def solicitar_adopcion(request, perro_id):
    """Vista para solicitar la adopción de un perro"""
    perro = get_object_or_404(Perro, id=perro_id, estado='disponible')
    
    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.perro = perro
            solicitud.save()
            messages.success(request, f'¡Hemos recibido tu solicitud para adoptar a {perro.nombre}! Te contactaremos pronto.')
            return redirect('adopciones:detalle_perro', perro_id=perro.id)
    else:
        form = SolicitudAdopcionForm()
    
    context = {
        'form': form,
        'perro': perro,
    }
    
    return render(request, 'adopciones/solicitar_adopcion.html', context)
