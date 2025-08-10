from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Perro, SolicitudAdopcion
from .forms import SolicitudAdopcionForm, FiltroPerrosForm

def lista_perros(request):
    """Vista para mostrar la lista de perros disponibles"""
    # Inicializar el formulario con los datos GET
    form = FiltroPerrosForm(request.GET)
    perros = Perro.objects.filter(estado='disponible')
    
    
    # Aplicar filtros si hay datos en el formulario
    if form.is_bound and form.data:
        # Validar el formulario para obtener cleaned_data
        if form.is_valid():
            
            # Filtrar por tamaño
            tamano = form.cleaned_data.get('tamano')
            if tamano:
                perros = perros.filter(tamano=tamano)
            
            # Filtrar por sexo
            sexo = form.cleaned_data.get('sexo')
            if sexo:
                perros = perros.filter(sexo=sexo)
            
            # Filtrar por color
            color = form.cleaned_data.get('color')
            if color:
                perros = perros.filter(color=color)
            
            # Filtrar por edad mínima
            edad_min = form.cleaned_data.get('edad_min')
            if edad_min is not None:
                perros = perros.filter(edad__gte=edad_min)
            
            # Filtrar por edad máxima
            edad_max = form.cleaned_data.get('edad_max')
            if edad_max is not None:
                perros = perros.filter(edad__lte=edad_max)
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    
    # Paginación
    paginator = Paginator(perros, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'perros': page_obj,
        'form': form,
        'total_perros': perros.count(),
    }
    
    # Si es una petición AJAX, devolver solo el contenido necesario
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'adopciones/partial_perros.html', context)
    
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
        # Debug: imprimir datos POST
        print("=== DEBUG POST DATA ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        print("=========================")
        
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.perro = perro
            solicitud.save()
            
            # Debug: imprimir datos guardados
            print("=== DEBUG DATOS GUARDADOS ===")
            print(f"Vivienda tipo: {solicitud.vivienda_tipo}")
            print(f"Patio: {solicitud.patio}")
            print("==============================")
            
            messages.success(request, f'¡Hemos recibido tu solicitud para adoptar a {perro.nombre}! Te contactaremos pronto.')
            return redirect('adopciones:detalle_perro', perro_id=perro.id)
        else:
            # Debug: imprimir errores del formulario
            print("=== DEBUG ERRORES FORMULARIO ===")
            print(form.errors)
            print("=================================")
    else:
        form = SolicitudAdopcionForm()
    
    context = {
        'form': form,
        'perro': perro,
    }
    
    return render(request, 'adopciones/solicitar_adopcion.html', context)
