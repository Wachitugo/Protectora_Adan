# 🐕 Protectora Adán - Landing Page

Una landing page completa para el albergue de perros "Protectora Adán", desarrollada con Django y Docker, con siste## 🔧 Configuración

### 🗄️ Base de Datos SQLite

La aplicación utiliza **SQLite optimizada para producción** con las siguientes ventajas:
- **Simplicidad**: Sin servidor de BD separado
- **Rendimiento**: Optimizada para aplicaciones medianas
- **Backup**: Simple copia de archivo
- **Costo**: Sin gastos adicionales de hosting

#### Optimizaciones Implementadas:
- **WAL Mode**: Mejor concurrencia para lecturas
- **Cache optimizado**: 8MB de cache para mejor rendimiento
- **Memory mapping**: 256MB para acceso rápido
- **Timeouts configurados**: Evita bloqueos

> 📚 Ver documentación completa en `docs/SQLITE_PRODUCTION.md`

### Variables de Entornode donaciones WebPay integrado.

## 🌟 Características

### Funcionalidades Principales
- **🏠 Página de Inicio**: Hero section con información destacada y estadísticas
- **📋 Sobre Nosotros**: Información detallada del albergue, misión y visión
- **🐕 Adopciones**: Catálogo de perros disponibles con filtros avanzados
- ** Donaciones**: Sistema completo con WebPay de Transbank (pesos chilenos)
- **📢 Avisos**: Sistema de noticias y avisos importantes
- **🤝 Voluntariado**: Formulario para solicitar ser voluntario
- **📱 Redes Sociales**: Integración con redes sociales
- **📱 Responsive**: Diseño adaptable a todos los dispositivos

### 💳 Sistema de Pagos WebPay
- **Integración con Transbank**: Procesamiento seguro de pagos
- **Moneda Chilena**: Donaciones en pesos chilenos (CLP)
- **Tarjetas Compatibles**: Visa, Mastercard, Redcompra
- **Estados de Transacción**: Seguimiento completo de pagos
- **Comprobantes**: Generación automática de recibos

### Tecnologías Utilizadas
- **Backend**: Django 4.2.7
- **Pagos**: WebPay de Transbank (transbank-sdk 6.1.0)
- **Base de Datos**: SQLite (optimizada para producción)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Formularios**: Django Crispy Forms con Bootstrap 5
- **Contenedores**: Docker y Docker Compose
- **Archivos Estáticos**: WhiteNoise
- **Imágenes**: Pillow para manejo de imágenes

## 🚀 Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose
- Git

### Configuración Local con Docker

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd pagina-albergue
```

2. **Construir y ejecutar con Docker Compose**
```bash
docker-compose up --build
```

3. **Acceder a la aplicación**
- Aplicación: http://localhost:8000
- Admin: http://localhost:8000/admin

4. **Crear superusuario** (en otra terminal)
```bash
docker-compose exec web python manage.py createsuperuser
```

### Configuración para Desarrollo Local (sin Docker)

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

## 🏗️ Estructura del Proyecto

```
protectora_adan/
├── core/                   # Aplicación principal
│   ├── models.py          # Modelos de información del albergue
│   ├── views.py           # Vistas principales
│   ├── forms.py           # Formularios
│   └── admin.py           # Configuración del admin
├── adopciones/            # Aplicación de adopciones
│   ├── models.py          # Modelos de perros y solicitudes
│   ├── views.py           # Vistas de adopción
│   ├── forms.py           # Formularios de adopción
│   └── admin.py           # Admin de adopciones
├── donaciones/            # Aplicación de donaciones
│   ├── models.py          # Modelos de donaciones con WebPay
│   ├── views.py           # Vistas de donaciones y WebPay
│   ├── forms.py           # Formularios de donación
│   ├── webpay_service.py  # Servicio de integración WebPay
│   ├── webpay_config.py   # Configuración de WebPay
│   └── admin.py           # Admin de donaciones
├── templates/             # Plantillas HTML
├── static/                # Archivos estáticos
├── media/                 # Archivos de usuario
├── protectora_adan/       # Configuración del proyecto
└── requirements.txt       # Dependencias
```

## 📱 Funcionalidades Detalladas

### Sistema de Adopciones
- **Catálogo de Perros**: Lista completa con paginación
- **Filtros Avanzados**: Por tamaño, sexo, color, edad
- **Detalles del Perro**: Información completa con fotos
- **Solicitudes de Adopción**: Formulario detallado

### 💳 Sistema de Donaciones con WebPay
- **Procesamiento Seguro**: Integración oficial con Transbank
- **Montos Sugeridos**: $10.000, $25.000, $50.000, $100.000, $200.000 CLP
- **Tipos de Donación**: Diferentes categorías configurables
- **Estados de Pago**: Pendiente, completado, fallido
- **Comprobantes**: Con código de autorización y detalles
- **Modo Desarrollo**: Tarjetas de prueba para testing

### 🧪 Testing de WebPay
- **Tarjetas de Prueba**:
  - Visa: `4051 8856 0000 0008`
  - Mastercard: `5186 0595 5959 0568`
  - Redcompra: `4001 0000 0000 0002`
- **CVV**: Cualquier 3 dígitos
- **Fecha**: Cualquier fecha futura

### Panel de Administración
- **Gestión de Perros**: CRUD completo con estados
- **Solicitudes**: Revisión y aprobación de adopciones
- **Donaciones**: Seguimiento y gestión
- **Avisos**: Publicación de noticias importantes
- **Voluntarios**: Gestión de solicitudes

##  Configuración

### Variables de Entorno

```bash
# Desarrollo
DEBUG=True
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# WebPay (Credenciales de prueba)
BASE_URL=http://localhost:8000
WEBPAY_PLUS_COMMERCE_CODE=597055555532
WEBPAY_PLUS_API_KEY=579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C
WEBPAY_PRODUCTION=False
```

### 🧪 Probar WebPay Localmente

1. **Verificar configuración**
```bash
python test_webpay.py
```

2. **Acceder a vista de prueba** (como admin)
```
http://localhost:8000/donaciones/webpay/test/
```

3. **Realizar donación de prueba**
```
http://localhost:8000/donaciones/donar/
```

### 🛠️ Mantenimiento de SQLite

Para optimizar y mantener la base de datos:

```bash
# Ejecutar mantenimiento (backup + optimización)
python scripts/sqlite_maintenance.py

# El script automáticamente:
# - Crea backup con timestamp
# - Verifica integridad
# - Optimiza la base de datos (VACUUM + ANALYZE)
# - Muestra estadísticas
```

**Recomendación**: Ejecutar mensualmente o cuando la BD supere 100MB.

## 📊 Modelos de Datos

### Perro
- Información básica (nombre, edad, raza)
- Características físicas (tamaño, color, peso)
- Estado de salud (vacunado, esterilizado)
- Comportamiento (bueno con niños, otros perros)
- Estado de adopción

### Solicitud de Adopción
- Información del solicitante
- Detalles de la vivienda
- Experiencia con mascotas
- Estado de la solicitud

### Donación
- Tipo de donación
- Información del donante
- Cantidad y estado
- Opción de anonimato

## 🎨 Personalización

### Colores y Tema
Los colores principales se definen en `static/css/style.css`:
```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --success-color: #198754;
    /* ... */
}
```

### Logo y Branding
- Agregar logo en `static/img/logo.png`
- Actualizar información en `core/models.py` → `InformacionAlbergue`

## 🔒 Seguridad

- ✅ CSRF Protection
- ✅ SQL Injection Protection (Django ORM)
- ✅ XSS Protection
- ✅ Secure Headers
- ✅ Environment Variables para secrets
- ✅ WhiteNoise para archivos estáticos seguros

## 📈 Mejoras Futuras

- [ ] Sistema de reservas online
- [ ] Chat en tiempo real
- [ ] API REST para móvil
- [ ] Sistema de notificaciones
- [ ] Integración con redes sociales
- [ ] Blog/CMS
- [ ] Sistema de voluntarios avanzado
- [ ] Reportes y analytics

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Soporte

Para soporte o preguntas:
- 📧 Email: soporte@protectoraadan.es
- 📱 WhatsApp: +56 9 XXXX XXXX
- 🐛 Issues: GitHub Issues

---

Desarrollado con ❤️ para la Protectora Adán
