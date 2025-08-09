# 🐕 Protectora Adán - Landing Page

Una landing page completa para el albergue de perros "Protectora Adán", desarrollada con Django y Docker, lista para desplegar en Azure Container Apps.

## 🌟 Características

### Funcionalidades Principales
- **🏠 Página de Inicio**: Hero section con información destacada y estadísticas
- **📋 Sobre Nosotros**: Información detallada del albergue, misión y visión
- **🐕 Adopciones**: Catálogo de perros disponibles con filtros avanzados
- **💝 Sistema de Match**: Algoritmo para encontrar el perro perfecto según preferencias
- **💰 Donaciones**: Sistema de donaciones con diferentes tipos
- **📢 Avisos**: Sistema de noticias y avisos importantes
- **🤝 Voluntariado**: Formulario para solicitar ser voluntario
- **📱 Redes Sociales**: Integración con redes sociales
- **📱 Responsive**: Diseño adaptable a todos los dispositivos

### Tecnologías Utilizadas
- **Backend**: Django 4.2.7
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
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
│   ├── views.py           # Vistas de adopción y match
│   ├── forms.py           # Formularios de adopción
│   └── admin.py           # Admin de adopciones
├── donaciones/            # Aplicación de donaciones
│   ├── models.py          # Modelos de donaciones y avisos
│   ├── views.py           # Vistas de donaciones
│   ├── forms.py           # Formularios de donación
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
- **Sistema de Match**: Algoritmo de compatibilidad

### Sistema de Donaciones
- **Tipos de Donación**: Diferentes categorías configurables
- **Formulario de Donación**: Con información del donante
- **Donaciones Anónimas**: Opción de anonimato
- **Seguimiento**: Estado de las donaciones

### Panel de Administración
- **Gestión de Perros**: CRUD completo con estados
- **Solicitudes**: Revisión y aprobación de adopciones
- **Donaciones**: Seguimiento y gestión
- **Avisos**: Publicación de noticias importantes
- **Voluntarios**: Gestión de solicitudes

## 🐳 Despliegue en Azure Container Apps

### Configuración de Producción

1. **Crear archivo de configuración para Azure**
```yaml
# azure-container-app.yaml
properties:
  managedEnvironmentId: /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.App/managedEnvironments/{env-name}
  configuration:
    ingress:
      external: true
      targetPort: 8000
    secrets:
      - name: "django-secret-key"
        value: "tu-clave-secreta-segura"
      - name: "database-url"
        value: "postgresql://usuario:password@host:puerto/basedatos"
  template:
    containers:
      - image: tu-registry.azurecr.io/protectora-adan:latest
        name: protectora-adan
        env:
          - name: "SECRET_KEY"
            secretRef: "django-secret-key"
          - name: "DATABASE_URL"
            secretRef: "database-url"
          - name: "DEBUG"
            value: "False"
          - name: "ALLOWED_HOSTS"
            value: "tu-app.azurecontainerapps.io"
        resources:
          cpu: 0.25
          memory: 0.5Gi
```

2. **Configurar base de datos PostgreSQL**
```bash
# Crear Azure Database for PostgreSQL
az postgres server create \
  --name protectora-adan-db \
  --resource-group tu-grupo \
  --admin-user admin_user \
  --admin-password tu_password
```

3. **Construir y subir imagen**
```bash
# Construir imagen
docker build -t protectora-adan .

# Etiquetar para Azure Container Registry
docker tag protectora-adan tu-registry.azurecr.io/protectora-adan:latest

# Subir imagen
docker push tu-registry.azurecr.io/protectora-adan:latest
```

4. **Desplegar en Azure Container Apps**
```bash
az containerapp create \
  --name protectora-adan \
  --resource-group tu-grupo \
  --environment tu-environment \
  --image tu-registry.azurecr.io/protectora-adan:latest
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Desarrollo
DEBUG=True
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Producción
DEBUG=False
SECRET_KEY=clave-super-segura-para-produccion
DATABASE_URL=postgresql://usuario:password@host:puerto/basedatos
ALLOWED_HOSTS=tu-dominio.azurecontainerapps.io
```

### Configuración de Media Files en Azure
Para archivos de usuario (imágenes), se recomienda usar Azure Blob Storage:

```python
# settings.py para producción
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = 'tu-storage-account'
AZURE_ACCOUNT_KEY = 'tu-key'
AZURE_CONTAINER = 'media'
```

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

- [ ] Sistema de pagos en línea (Stripe/PayPal)
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
- 📱 WhatsApp: +34 XXX XXX XXX
- 🐛 Issues: GitHub Issues

---

Desarrollado con ❤️ para la Protectora Adán
