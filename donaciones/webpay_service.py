"""
Servicio para integración con WebPay de Transbank
"""
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid
import logging
from .webpay_config import (
    WEBPAY_PLUS_COMMERCE_CODE, 
    WEBPAY_PLUS_API_KEY, 
    WEBPAY_PRODUCTION,
    BASE_URL
)
from .models import Donacion

logger = logging.getLogger(__name__)

class WebPayService:
    """Servicio para manejar transacciones WebPay"""
    
    def __init__(self):
        """Inicializar configuración de WebPay"""
        # Configurar opciones
        integration_type = IntegrationType.LIVE if WEBPAY_PRODUCTION else IntegrationType.TEST
        
        options = WebpayOptions(
            commerce_code=WEBPAY_PLUS_COMMERCE_CODE,
            api_key=WEBPAY_PLUS_API_KEY,
            integration_type=integration_type
        )
        
        # Crear instancia de Transaction con opciones
        self.transaction = Transaction(options)
    
    def create_transaction(self, donacion):
        """
        Crear una transacción WebPay para una donación
        
        Args:
            donacion: Instancia del modelo Donacion
            
        Returns:
            dict: Respuesta con token y URL de WebPay
        """
        try:
            # Generar orden de compra única
            buy_order = f"DON-{donacion.id}-{uuid.uuid4().hex[:8]}"
            session_id = str(uuid.uuid4())
            
            # URLs de retorno
            return_url = BASE_URL + reverse('donaciones:webpay_resultado')
            
            logger.info(f"Creando transacción WebPay - Monto: {donacion.cantidad}, Return URL: {return_url}")
            
            # Crear transacción usando la instancia
            response = self.transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=int(donacion.cantidad),  # WebPay requiere entero
                return_url=return_url
            )
            
            # Actualizar donación con datos de WebPay
            donacion.buy_order = buy_order
            donacion.session_id = session_id
            donacion.token_ws = response['token']
            donacion.save()
            
            logger.info(f"Transacción WebPay creada para donación {donacion.id}")
            
            return {
                'success': True,
                'token': response['token'],
                'url': response['url']
            }
            
        except Exception as e:
            logger.error(f"Error al crear transacción WebPay: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_transaction(self, token):
        """
        Confirmar una transacción WebPay
        
        Args:
            token: Token de la transacción
            
        Returns:
            dict: Resultado de la confirmación
        """
        try:
            # Confirmar transacción usando la instancia
            response = self.transaction.commit(token)
            
            # Buscar donación por token
            try:
                donacion = Donacion.objects.get(token_ws=token)
            except Donacion.DoesNotExist:
                logger.error(f"No se encontró donación con token {token}")
                return {
                    'success': False,
                    'error': 'Donación no encontrada'
                }
            
            # Actualizar donación con respuesta de WebPay
            donacion.webpay_response = response
            donacion.authorization_code = response.get('authorization_code', '')
            donacion.transaction_date = timezone.now()
            
            # Verificar estado de la transacción
            if response.get('response_code') == 0:  # Transacción exitosa
                donacion.estado = 'completada'
                donacion.save()
                
                logger.info(f"Transacción confirmada para donación {donacion.id}")
                
                return {
                    'success': True,
                    'donacion': donacion,
                    'response': response
                }
            else:
                donacion.estado = 'fallida'
                donacion.save()
                
                logger.warning(f"Transacción fallida para donación {donacion.id}")
                
                return {
                    'success': False,
                    'donacion': donacion,
                    'response': response,
                    'error': 'Transacción rechazada'
                }
                
        except Exception as e:
            logger.error(f"Error al confirmar transacción WebPay: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_transaction_status(self, token):
        """
        Obtener estado de una transacción WebPay
        
        Args:
            token: Token de la transacción
            
        Returns:
            dict: Estado de la transacción
        """
        try:
            response = self.transaction.status(token)
            return {
                'success': True,
                'status': response
            }
        except Exception as e:
            logger.error(f"Error al obtener estado de transacción: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
