"""
Configuración para WebPay de Transbank
"""
from decouple import config

# Configuración de WebPay
WEBPAY_PLUS_COMMERCE_CODE = config('WEBPAY_PLUS_COMMERCE_CODE', default='597055555532')
WEBPAY_PLUS_API_KEY = config('WEBPAY_PLUS_API_KEY', default='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C')

# URLs de retorno
BASE_URL = config('BASE_URL', default='http://localhost:8000')
WEBPAY_RETURN_URL = f"{BASE_URL}/donaciones/webpay/resultado/"
WEBPAY_FINAL_URL = f"{BASE_URL}/donaciones/gracias/"

# Configuración del entorno (True para producción, False para desarrollo)
WEBPAY_PRODUCTION = config('WEBPAY_PRODUCTION', default=False, cast=bool)

# Configuración de tiempo de sesión (en segundos)
WEBPAY_SESSION_TIMEOUT = 300  # 5 minutos
