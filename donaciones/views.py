from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging
from .models import TipoDonacion, Donacion, Aviso
from .forms import DonacionForm
from .webpay_service import WebPayService

logger = logging.getLogger(__name__)

def donar(request):
    """Vista para realizar donaciones"""
    tipos_donacion = TipoDonacion.objects.filter(activo=True)
    
    if request.method == 'POST':
        logger.info("=== INICIO PROCESO DONACIÓN ===")
        logger.info(f"POST data: {request.POST}")
        
        form = DonacionForm(request.POST)
        if form.is_valid():
            logger.info("Formulario válido, procesando donación...")
            try:
                donacion = form.save(commit=False)
                donacion.estado = 'pendiente'
                donacion.save()
                
                logger.info(f"Donación creada: ID {donacion.id}, Monto: ${donacion.cantidad}")
                
                # Inicializar servicio WebPay
                webpay_service = WebPayService()
                
                # Crear transacción WebPay
                result = webpay_service.create_transaction(donacion)
                logger.info(f"Resultado WebPay: {result}")
                
                if result['success']:
                    # Redirigir a WebPay
                    webpay_url = f"{result['url']}?token_ws={result['token']}"
                    logger.info(f"Redirigiendo a WebPay: {webpay_url}")
                    return redirect(webpay_url)
                else:
                    # Error al crear transacción
                    logger.error(f"Error al crear transacción WebPay: {result.get('error', 'Error desconocido')}")
                    messages.error(
                        request, 
                        'Error al procesar el pago. Por favor, inténtalo de nuevo.'
                    )
                    donacion.delete()  # Eliminar donación fallida
            except Exception as e:
                logger.error(f"Error en proceso de donación: {str(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                messages.error(
                    request, 
                    'Ocurrió un error inesperado. Por favor, inténtalo de nuevo.'
                )
        else:
            logger.error(f"Formulario de donación inválido: {form.errors}")
            messages.error(request, f"Error en el formulario: {form.errors}")
    else:
        form = DonacionForm()
    
    context = {
        'form': form,
        'tipos_donacion': tipos_donacion,
    }
    
    return render(request, 'donaciones/donar.html', context)

def gracias(request, donacion_id):
    """Vista de agradecimiento después de una donación"""
    try:
        donacion = Donacion.objects.get(id=donacion_id)
    except Donacion.DoesNotExist:
        return redirect('donaciones:donar')
    
    context = {
        'donacion': donacion,
    }
    
    return render(request, 'donaciones/gracias.html', context)

def avisos(request):
    """Vista para mostrar todos los avisos"""
    avisos_list = Aviso.objects.filter(activo=True).order_by('-fecha_creacion')
    
    context = {
        'avisos': avisos_list,
    }
    
    return render(request, 'donaciones/avisos.html', context)

def webpay_resultado(request):
    """Vista para procesar el resultado de WebPay"""
    token_ws = request.GET.get('token_ws')
    
    if not token_ws:
        messages.error(request, 'Error en el proceso de pago.')
        return redirect('donaciones:donar')
    
    # Inicializar servicio WebPay
    webpay_service = WebPayService()
    
    # Confirmar transacción
    result = webpay_service.confirm_transaction(token_ws)
    
    if result['success']:
        donacion = result['donacion']
        messages.success(
            request, 
            f'¡Pago exitoso! Gracias por tu donación de ${donacion.cantidad:,.0f} CLP.'
        )
        return redirect('donaciones:gracias', donacion_id=donacion.id)
    else:
        if 'donacion' in result:
            donacion = result['donacion']
            messages.error(
                request, 
                'El pago no pudo ser procesado. Por favor, inténtalo de nuevo.'
            )
            return redirect('donaciones:gracias', donacion_id=donacion.id)
        else:
            messages.error(request, 'Error en el proceso de pago.')
            return redirect('donaciones:donar')

def webpay_error(request):
    """Vista para manejar errores de WebPay"""
    messages.error(request, 'Ocurrió un error durante el proceso de pago.')
    return redirect('donaciones:donar')

def test_webpay_config(request):
    """Vista de prueba para verificar configuración de WebPay"""
    if not request.user.is_superuser:
        return redirect('donaciones:donar')
    
    try:
        from .webpay_config import WEBPAY_PLUS_COMMERCE_CODE, WEBPAY_PLUS_API_KEY, WEBPAY_PRODUCTION, BASE_URL
        
        config_info = {
            'commerce_code': WEBPAY_PLUS_COMMERCE_CODE,
            'api_key': WEBPAY_PLUS_API_KEY[:20] + '...',  # Solo mostrar parte de la key
            'production': WEBPAY_PRODUCTION,
            'base_url': BASE_URL,
        }
        
        # Intentar importar Transbank
        from transbank.webpay.webpay_plus.transaction import Transaction
        from transbank.common.integration_type import IntegrationType
        
        # Configurar
        Transaction.integration_type = IntegrationType.TEST
        Transaction.commerce_code = WEBPAY_PLUS_COMMERCE_CODE
        Transaction.api_key = WEBPAY_PLUS_API_KEY
        
        context = {
            'config_info': config_info,
            'transbank_imported': True,
            'status': 'OK - Configuración cargada correctamente'
        }
        
    except Exception as e:
        context = {
            'error': str(e),
            'status': 'ERROR - Problema en la configuración'
        }
    
    return render(request, 'donaciones/test_webpay.html', context)
