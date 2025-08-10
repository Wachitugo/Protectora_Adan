# 🧪 Guía de Testing para Protectora Adán

## 📋 Estrategia de Testing

### Niveles de Testing
1. **Unit Tests**: Modelos, vistas individuales, funciones
2. **Integration Tests**: Workflows completos, APIs
3. **E2E Tests**: Experiencia completa del usuario
4. **Performance Tests**: Carga y rendimiento

## 🔧 Configuración de Testing

### 1. Dependencias para Testing
Agregar a `requirements-test.txt`:
```
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
pytest-mock==3.12.0
selenium==4.15.2
locust==2.17.0
```

### 2. Configuración pytest
Crear `pytest.ini`:
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = protectora_adan.settings_test
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --no-migrations --reuse-db --cov=. --cov-report=html --cov-report=term
```

### 3. Settings para Testing
Crear `protectora_adan/settings_test.py`:
```python
from .settings import *

# Base de datos en memoria para tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Desactivar migraciones para velocidad
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Email backend para testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Password hasher más rápido para tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Media root temporal
MEDIA_ROOT = '/tmp/test_media'

# WebPay en modo testing
WEBPAY_PRODUCTION = False
WEBPAY_PLUS_COMMERCE_CODE = '597055555532'
WEBPAY_PLUS_API_KEY = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
```

## 🧪 Tests Unitarios

### 1. Tests de Modelos
Crear `core/tests/test_models.py`:
```python
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Perro, SolicitudAdopcion

class PerroModelTest(TestCase):
    def test_perro_creation(self):
        """Test que un perro se crea correctamente"""
        perro = Perro.objects.create(
            nombre="Bobby",
            edad=3,
            raza="Mestizo",
            descripcion="Perro amigable",
            adoptado=False
        )
        self.assertEqual(perro.nombre, "Bobby")
        self.assertEqual(perro.edad, 3)
        self.assertFalse(perro.adoptado)
    
    def test_perro_str_method(self):
        """Test del método __str__ del modelo Perro"""
        perro = Perro.objects.create(
            nombre="Luna",
            edad=2,
            raza="Golden Retriever"
        )
        self.assertEqual(str(perro), "Luna")
    
    def test_perro_edad_validation(self):
        """Test que la edad no puede ser negativa"""
        with self.assertRaises(ValidationError):
            perro = Perro(
                nombre="Test",
                edad=-1,
                raza="Test"
            )
            perro.full_clean()

class SolicitudAdopcionModelTest(TestCase):
    def setUp(self):
        self.perro = Perro.objects.create(
            nombre="Max",
            edad=4,
            raza="Labrador"
        )
    
    def test_solicitud_creation(self):
        """Test que una solicitud se crea correctamente"""
        solicitud = SolicitudAdopcion.objects.create(
            perro=self.perro,
            nombre_adoptante="Juan Pérez",
            email="juan@email.com",
            telefono="123456789",
            experiencia="Tengo experiencia con perros"
        )
        self.assertEqual(solicitud.nombre_adoptante, "Juan Pérez")
        self.assertEqual(solicitud.perro, self.perro)
        self.assertFalse(solicitud.aprobada)
```

### 2. Tests de Vistas
Crear `adopciones/tests/test_views.py`:
```python
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Perro, SolicitudAdopcion

class AdopcionesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.perro = Perro.objects.create(
            nombre="Buddy",
            edad=2,
            raza="Mestizo",
            descripcion="Perro muy cariñoso"
        )
    
    def test_lista_perros_view(self):
        """Test de la vista lista de perros"""
        response = self.client.get(reverse('adopciones:lista_perros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Buddy")
    
    def test_detalle_perro_view(self):
        """Test de la vista detalle del perro"""
        response = self.client.get(
            reverse('adopciones:detalle_perro', args=[self.perro.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.perro.nombre)
    
    def test_solicitar_adopcion_get(self):
        """Test GET de solicitud de adopción"""
        response = self.client.get(
            reverse('adopciones:solicitar_adopcion', args=[self.perro.id])
        )
        self.assertEqual(response.status_code, 200)
    
    def test_solicitar_adopcion_post_valid(self):
        """Test POST válido de solicitud de adopción"""
        data = {
            'nombre_adoptante': 'María García',
            'email': 'maria@email.com',
            'telefono': '987654321',
            'experiencia': 'He tenido perros toda mi vida'
        }
        response = self.client.post(
            reverse('adopciones:solicitar_adopcion', args=[self.perro.id]),
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect después de éxito
        self.assertTrue(
            SolicitudAdopcion.objects.filter(
                email='maria@email.com'
            ).exists()
        )
    
    def test_solicitar_adopcion_post_invalid(self):
        """Test POST inválido de solicitud de adopción"""
        data = {
            'nombre_adoptante': '',  # Campo requerido vacío
            'email': 'email_invalido',
            'telefono': '123'
        }
        response = self.client.post(
            reverse('adopciones:solicitar_adopcion', args=[self.perro.id]),
            data
        )
        self.assertEqual(response.status_code, 200)  # Se queda en la página con errores
        self.assertFalse(
            SolicitudAdopcion.objects.filter(
                perro=self.perro
            ).exists()
        )
```

### 3. Tests de Donaciones
Crear `donaciones/tests/test_webpay.py`:
```python
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from donaciones.models import Donacion

class WebPayIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    @patch('donaciones.views.Transaction')
    def test_crear_donacion_view(self, mock_transaction):
        """Test de creación de donación con WebPay"""
        # Mock de la respuesta de WebPay
        mock_instance = MagicMock()
        mock_instance.create.return_value = {
            'token': 'test_token_123',
            'url': 'https://webpay3gint.transbank.cl/webpayserver/initTransaction'
        }
        mock_transaction.return_value = mock_instance
        
        data = {
            'monto': 10000,
            'nombre_donante': 'Carlos López',
            'email': 'carlos@email.com'
        }
        
        response = self.client.post(reverse('donaciones:crear_donacion'), data)
        
        # Verificar que se redirige a WebPay
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó la donación
        donacion = Donacion.objects.get(email='carlos@email.com')
        self.assertEqual(donacion.monto, 10000)
        self.assertEqual(donacion.estado, 'pendiente')
    
    @patch('donaciones.views.Transaction')
    def test_retorno_webpay_exitoso(self, mock_transaction):
        """Test de retorno exitoso desde WebPay"""
        # Crear donación previa
        donacion = Donacion.objects.create(
            monto=5000,
            nombre_donante='Ana Silva',
            email='ana@email.com',
            token_ws='test_token_456',
            estado='pendiente'
        )
        
        # Mock de la respuesta de confirmación
        mock_instance = MagicMock()
        mock_instance.commit.return_value = {
            'response_code': 0,  # Éxito
            'transaction_date': '2024-01-15T10:30:00.000Z',
            'authorization_code': 'AUTH123',
            'amount': 5000
        }
        mock_transaction.return_value = mock_instance
        
        response = self.client.get(
            reverse('donaciones:retorno_webpay'),
            {'token_ws': 'test_token_456'}
        )
        
        # Verificar redirección a éxito
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se actualizó la donación
        donacion.refresh_from_db()
        self.assertEqual(donacion.estado, 'completada')
    
    def test_retorno_webpay_cancelado(self):
        """Test de retorno cuando el usuario cancela"""
        donacion = Donacion.objects.create(
            monto=3000,
            nombre_donante='Pedro Ruiz',
            email='pedro@email.com',
            token_ws='test_token_789',
            estado='pendiente'
        )
        
        response = self.client.get(
            reverse('donaciones:retorno_webpay'),
            {'TBK_TOKEN': 'test_token_789'}  # Parámetro de cancelación
        )
        
        # Verificar redirección a cancelación
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se actualizó el estado
        donacion.refresh_from_db()
        self.assertEqual(donacion.estado, 'cancelada')
```

## 🔗 Tests de Integración

### 1. Test de Workflow Completo
Crear `tests/test_integration.py`:
```python
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Perro, SolicitudAdopcion

class AdoptionWorkflowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.perro = Perro.objects.create(
            nombre="Rex",
            edad=3,
            raza="Pastor Alemán",
            descripcion="Perro guardián muy leal"
        )
    
    def test_complete_adoption_workflow(self):
        """Test del workflow completo de adopción"""
        # 1. Ver lista de perros
        response = self.client.get(reverse('adopciones:lista_perros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rex")
        
        # 2. Ver detalle del perro
        response = self.client.get(
            reverse('adopciones:detalle_perro', args=[self.perro.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pastor Alemán")
        
        # 3. Solicitar adopción
        adoption_data = {
            'nombre_adoptante': 'Laura Martínez',
            'email': 'laura@email.com',
            'telefono': '555-0123',
            'experiencia': 'Tengo experiencia con perros grandes'
        }
        
        response = self.client.post(
            reverse('adopciones:solicitar_adopcion', args=[self.perro.id]),
            adoption_data
        )
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar que se creó la solicitud
        solicitud = SolicitudAdopcion.objects.get(email='laura@email.com')
        self.assertEqual(solicitud.perro, self.perro)
        self.assertEqual(solicitud.nombre_adoptante, 'Laura Martínez')
        self.assertFalse(solicitud.aprobada)
        
        # 5. El perro aún no debe estar marcado como adoptado
        self.perro.refresh_from_db()
        self.assertFalse(self.perro.adoptado)

class DonationWorkflowTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_donation_form_validation(self):
        """Test de validación del formulario de donación"""
        # Datos inválidos
        invalid_data = {
            'monto': 500,  # Menos del mínimo
            'nombre_donante': '',
            'email': 'email_invalido'
        }
        
        response = self.client.post(
            reverse('donaciones:crear_donacion'),
            invalid_data
        )
        
        # Debe quedarse en la página con errores
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')
```

## 🌐 Tests End-to-End con Selenium

### 1. Configuración Selenium
Crear `tests/test_e2e.py`:
```python
import pytest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from core.models import Perro

class E2EAdoptionTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar sin GUI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(options=chrome_options)
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def setUp(self):
        self.perro = Perro.objects.create(
            nombre="Toby",
            edad=2,
            raza="Beagle",
            descripcion="Perro muy juguetón"
        )
    
    def test_user_can_view_and_adopt_dog(self):
        """Test E2E: usuario puede ver y solicitar adopción"""
        # Ir a la página principal
        self.selenium.get(f'{self.live_server_url}/')
        
        # Verificar que la página carga
        self.assertIn("Protectora Adán", self.selenium.title)
        
        # Ir a la lista de perros
        adopciones_link = self.selenium.find_element(By.LINK_TEXT, "Adopciones")
        adopciones_link.click()
        
        # Verificar que aparece el perro
        self.assertIn("Toby", self.selenium.page_source)
        
        # Hacer clic en "Ver más"
        ver_mas_button = self.selenium.find_element(
            By.XPATH, f"//a[contains(@href, '/adopciones/detalle/{self.perro.id}/')]"
        )
        ver_mas_button.click()
        
        # Verificar que estamos en la página de detalle
        self.assertIn("Beagle", self.selenium.page_source)
        
        # Hacer clic en "Solicitar Adopción"
        solicitar_button = self.selenium.find_element(
            By.XPATH, "//a[contains(text(), 'Solicitar Adopción')]"
        )
        solicitar_button.click()
        
        # Llenar el formulario
        nombre_field = self.selenium.find_element(By.NAME, "nombre_adoptante")
        nombre_field.send_keys("Roberto González")
        
        email_field = self.selenium.find_element(By.NAME, "email")
        email_field.send_keys("roberto@email.com")
        
        telefono_field = self.selenium.find_element(By.NAME, "telefono")
        telefono_field.send_keys("555-9876")
        
        experiencia_field = self.selenium.find_element(By.NAME, "experiencia")
        experiencia_field.send_keys("He tenido beagles antes")
        
        # Enviar formulario
        submit_button = self.selenium.find_element(By.TYPE, "submit")
        submit_button.click()
        
        # Verificar mensaje de éxito
        wait = WebDriverWait(self.selenium, 10)
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        self.assertIn("éxito", success_message.text.lower())
```

## ⚡ Tests de Performance con Locust

### 1. Configuración Locust
Crear `tests/performance/locustfile.py`:
```python
from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Ejecutar al inicio de cada usuario"""
        pass
    
    @task(3)
    def view_homepage(self):
        """Visitar página principal"""
        self.client.get("/")
    
    @task(2)
    def view_dogs_list(self):
        """Ver lista de perros"""
        self.client.get("/adopciones/")
    
    @task(1)
    def view_dog_detail(self):
        """Ver detalle de perro aleatorio"""
        dog_id = random.randint(1, 10)  # Asumir que hay perros con IDs 1-10
        with self.client.get(f"/adopciones/detalle/{dog_id}/", catch_response=True) as response:
            if response.status_code == 404:
                response.success()  # No considerar 404 como error
    
    @task(1)
    def view_donation_form(self):
        """Ver formulario de donación"""
        self.client.get("/donaciones/")
    
    @task(1)
    def submit_adoption_form(self):
        """Enviar formulario de adopción"""
        dog_id = random.randint(1, 10)
        data = {
            'nombre_adoptante': f'Usuario Test {random.randint(1, 1000)}',
            'email': f'test{random.randint(1, 1000)}@email.com',
            'telefono': f'555{random.randint(1000, 9999)}',
            'experiencia': 'Experiencia de prueba'
        }
        with self.client.post(f"/adopciones/solicitar/{dog_id}/", data=data, catch_response=True) as response:
            if response.status_code in [200, 302, 404]:
                response.success()
```

### 2. Ejecutar Tests de Performance
```bash
# Instalar locust
pip install locust

# Ejecutar test
locust -f tests/performance/locustfile.py --host=http://localhost:8000

# Para CI/CD (sin interfaz web)
locust -f tests/performance/locustfile.py --host=http://localhost:8000 --headless -u 10 -r 2 -t 60s
```

## 🏃‍♂️ Ejecución de Tests

### 1. Tests Unitarios y de Integración
```bash
# Todos los tests
pytest

# Tests específicos
pytest core/tests/
pytest adopciones/tests/
pytest donaciones/tests/

# Con cobertura
pytest --cov=. --cov-report=html

# Tests específicos con verbose
pytest -v core/tests/test_models.py::PerroModelTest::test_perro_creation
```

### 2. Tests E2E
```bash
# Asegurar que chromedriver está en PATH
# Ejecutar tests E2E
pytest tests/test_e2e.py
```

### 3. Tests en Docker
Crear `docker-compose.test.yml`:
```yaml
version: '3.8'

services:
  test-db:
    image: postgres:13
    environment:
      POSTGRES_DB: test_protectora_adan
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    volumes:
      - test_db_data:/var/lib/postgresql/data

  test-app:
    build: .
    command: pytest
    volumes:
      - .:/app
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://test_user:test_password@test-db:5432/test_protectora_adan
    depends_on:
      - test-db

volumes:
  test_db_data:
```

```bash
# Ejecutar tests en Docker
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## 📊 Cobertura de Tests

### 1. Configurar coverage
Crear `.coveragerc`:
```ini
[run]
source = .
omit = 
    */venv/*
    */migrations/*
    manage.py
    protectora_adan/settings/*
    */tests/*
    */test_*.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### 2. Generar reportes
```bash
# Generar reporte HTML
pytest --cov=. --cov-report=html

# Generar reporte XML (para CI/CD)
pytest --cov=. --cov-report=xml

# Ver reporte en terminal
pytest --cov=. --cov-report=term-missing
```

## 🔄 CI/CD Testing Pipeline

### 1. GitHub Actions
Crear `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_protectora_adan
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_protectora_adan
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## 📝 Mejores Prácticas

### 1. Nomenclatura de Tests
- `test_model_creation()` - Creación de modelos
- `test_view_get_success()` - Vista GET exitosa
- `test_view_post_valid_data()` - POST con datos válidos
- `test_view_post_invalid_data()` - POST con datos inválidos
- `test_integration_complete_workflow()` - Workflow completo

### 2. Estructura de Tests
```python
class TestClass:
    def setUp(self):
        """Preparación antes de cada test"""
        pass
    
    def test_something(self):
        """Test con nombre descriptivo"""
        # Arrange (preparar)
        
        # Act (ejecutar)
        
        # Assert (verificar)
        pass
```

### 3. Datos de Prueba
- Usar factories para crear datos consistentes
- Evitar hardcodear valores específicos
- Usar datos realistas pero simples

### 4. Mocking
- Mockear servicios externos (WebPay, emails)
- No mockear código propio innecesariamente
- Verificar que los mocks se llamen correctamente

## 🎯 Objetivos de Cobertura

- **Unit Tests**: >80% cobertura de código
- **Integration Tests**: Workflows críticos cubiertos
- **E2E Tests**: Casos de uso principales
- **Performance Tests**: Endpoints críticos bajo carga

Esta guía te ayudará a mantener la calidad del código y detectar problemas antes de que lleguen a producción.
