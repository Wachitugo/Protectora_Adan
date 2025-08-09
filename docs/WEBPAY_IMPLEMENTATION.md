# 💳 Implementación de WebPay para Donaciones

## 🎯 Descripción
La aplicación ha sido configurada para procesar donaciones utilizando **WebPay de Transbank**, el sistema de pago más popular en Chile. Los usuarios pueden realizar donaciones seguras en pesos chilenos (CLP) utilizando tarjetas de crédito, débito y Redcompra.

## 🚀 Inicio Rápido

### 1. Verificar Configuración
1. Asegúrate de tener las variables de entorno configuradas en `.env`
2. Ejecuta el servidor: `python manage.py runserver`
3. Visita `http://localhost:8000/donaciones/webpay/test/` (como superusuario)
4. Verifica que la configuración esté correcta

### 2. Probar Flujo de Donación
1. Ve a `http://localhost:8000/donaciones/donar/`
2. Completa el formulario de donación
3. **Deberías ser redirigido automáticamente a la interfaz de WebPay**
4. Usa las tarjetas de prueba para completar el pago
5. Serás redirigido de vuelta a la página de agradecimiento

## ⚙️ Configuración

### Variables de Entorno
Agregar las siguientes variables a tu archivo `.env`:

```bash
# Configuración de WebPay (Transbank)
# Para desarrollo (credenciales de prueba)
WEBPAY_PLUS_COMMERCE_CODE=597055555532
WEBPAY_PLUS_API_KEY=579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
WEBPAY_PRODUCTION=False

# Para producción (reemplazar con credenciales reales)
# WEBPAY_PLUS_COMMERCE_CODE=tu_commerce_code_real
# WEBPAY_PLUS_API_KEY=tu_api_key_real
# WEBPAY_PRODUCTION=True

# URL base del sitio
BASE_URL=http://localhost:8000
```

### Dependencias
- `transbank-sdk==6.1.0`: SDK oficial de Transbank para Python
- `python-decouple==3.8`: Para manejo de variables de entorno

## Flujo de Donación

### 1. Formulario de Donación
- El usuario completa el formulario en `/donaciones/donar/`
- Se crea un registro de donación con estado "pendiente"
- Se redirige automáticamente a WebPay

### 2. Procesamiento en WebPay
- El usuario completa el pago en la plataforma segura de WebPay
- WebPay procesa el pago con los bancos chilenos
- WebPay redirige de vuelta a la aplicación

### 3. Confirmación de Pago
- La aplicación confirma la transacción con WebPay
- Se actualiza el estado de la donación según el resultado
- Se muestra la página de agradecimiento con detalles del pago

## Estados de Donación

- **pendiente**: Donación creada, esperando pago
- **completada**: Pago exitoso y confirmado
- **fallida**: Pago rechazado o con error

## Archivos Importantes

### Modelos (`donaciones/models.py`)
- Campos WebPay agregados: `token_ws`, `buy_order`, `session_id`, etc.
- Estados de donación actualizados

### Servicio WebPay (`donaciones/webpay_service.py`)
- `WebPayService`: Clase principal para manejar transacciones
- `create_transaction()`: Crea transacción en WebPay
- `confirm_transaction()`: Confirma y valida el pago

### Configuración (`donaciones/webpay_config.py`)
- Configuración centralizada de WebPay
- URLs de retorno y credenciales

### Vistas (`donaciones/views.py`)
- `donar()`: Procesa formulario y redirige a WebPay
- `webpay_resultado()`: Procesa respuesta de WebPay
- `webpay_error()`: Maneja errores de pago

### URLs (`donaciones/urls.py`)
- `/donaciones/webpay/resultado/`: Endpoint para respuesta de WebPay
- `/donaciones/webpay/error/`: Endpoint para errores

## Seguridad

### Validaciones
- Verificación de tokens WebPay
- Validación de montos y estados
- Logging de todas las transacciones

### Datos Protegidos
- Los datos de tarjetas nunca pasan por nuestro servidor
- WebPay maneja toda la información sensible
- Solo se almacenan tokens y códigos de autorización

## Testing

### Vista de Prueba
- URL: `/donaciones/webpay/test/` (solo para superusers)
- Verifica la configuración de WebPay
- Muestra estado de importaciones y credenciales

### Tarjetas de Prueba (Modo Desarrollo)
- **Visa**: 4051 8856 0000 0008
- **Mastercard**: 5186 0595 5959 0568  
- **Redcompra**: 4001 0000 0000 0002
- **CVV**: Cualquier 3 dígitos
- **Fecha**: Cualquier fecha futura

### Credenciales de Prueba
- Commerce Code: 597055555532
- API Key: 579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C

## Producción

### Obtener Credenciales Reales
1. Registrarse en Transbank
2. Completar proceso de certificación
3. Obtener Commerce Code y API Key
4. Configurar `WEBPAY_PRODUCTION=True`

### Certificación
- Transbank requiere certificación antes de usar en producción
- Proceso incluye pruebas de integración y validación

## Troubleshooting

### ❌ No se Redirige a WebPay
**Posibles Causas:**
1. Variables de entorno no configuradas en `.env`
2. SDK de Transbank no instalado: `pip install transbank-sdk`
3. Error en la configuración de URLs
4. Problema con la creación de transacción

**Solución:**
1. Verificar `/donaciones/webpay/test/` muestra configuración OK
2. Revisar logs del servidor para errores
3. Verificar que BASE_URL está correctamente configurada

### ❌ Error en el Pago
**Posibles Causas:**
1. Monto inválido (debe ser entero)
2. Credenciales incorrectas
3. URL de retorno incorrecta

**Solución:**
1. Verificar montos son números enteros
2. Usar tarjetas de prueba correctas
3. Verificar configuración en modo TEST

## Logs
Los eventos de WebPay se registran en el logger `donaciones`:
- Creación de transacciones
- Confirmaciones de pago
- Errores y excepciones

## Soporte
Para problemas con WebPay:
- Documentación oficial: https://transbank.github.io/transbank-sdk-python/
- Soporte Transbank: soporte@transbank.cl
