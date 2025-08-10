# 🗄️ SQLite en Producción - Protectora Adán

## 🎯 ¿Por qué SQLite para esta aplicación?

SQLite es una excelente opción para **Protectora Adán** porque:

- **Simplicidad**: Una sola aplicación web para un albergue
- **Tráfico Moderado**: Típicamente <100 usuarios concurrentes
- **Operaciones**: Principalmente lectura (catálogo de perros, información)
- **Escrituras Limitadas**: Donaciones y solicitudes de adopción ocasionales
- **Mantenimiento**: Sin necesidad de administrar servidor de BD separado

## ⚡ Optimizaciones Implementadas

### 1. Configuración de PRAGMA
```sql
PRAGMA foreign_keys=ON;        -- Integridad referencial
PRAGMA journal_mode=WAL;       -- Write-Ahead Logging (mejor concurrencia)
PRAGMA synchronous=NORMAL;     -- Balance entre seguridad y velocidad
PRAGMA temp_store=MEMORY;      -- Tablas temporales en memoria
PRAGMA cache_size=8000;        -- Cache de 8MB (8000 páginas de 1KB)
PRAGMA mmap_size=268435456;    -- Memory mapping de 256MB
```

### 2. Configuración Django
- **Timeout**: 30 segundos para conexiones
- **check_same_thread**: False para threading
- **WAL Mode**: Permite lecturas concurrentes

## 📊 Capacidades y Límites

### ✅ Capacidades
- **Usuarios Concurrentes**: Hasta 100-200 usuarios sin problemas
- **Tamaño de BD**: Hasta 1GB recomendado (281TB teórico)
- **Transacciones**: ACID completo
- **Velocidad**: Muy rápido para operaciones de lectura
- **Respaldo**: Simple copia de archivo

### ⚠️ Límites a Considerar
- **Un Escritor**: Solo una escritura simultánea
- **Sin Replicación**: No hay clustering nativo
- **Funciones**: Limitadas comparado con PostgreSQL
- **Tipos de Datos**: Menos tipos que otros SGBD

## 🔧 Mejores Prácticas

### 1. Estructura de Transacciones
```python
# ✅ Bueno: Transacciones cortas
with transaction.atomic():
    donacion.save()
    
# ❌ Evitar: Transacciones largas
# Bloquean la base de datos para otros escritores
```

### 2. Optimización de Consultas
```python
# ✅ Usar select_related para reducir consultas
perros = Perro.objects.select_related('raza').all()

# ✅ Usar prefetch_related para relaciones múltiples
perros = Perro.objects.prefetch_related('fotos').all()

# ✅ Paginación para listas grandes
paginator = Paginator(perros, 25)
```

### 3. Índices Importantes
```sql
-- Automáticos con Django
CREATE INDEX idx_perro_adoptado ON core_perro(adoptado);
CREATE INDEX idx_donacion_estado ON donaciones_donacion(estado);
CREATE INDEX idx_solicitud_fecha ON adopciones_solicitudadopcion(fecha_solicitud);
```

## 💾 Backup y Mantenimiento

### 1. Backup Automático
```bash
#!/bin/bash
# Script de backup diario
DATE=$(date +%Y%m%d_%H%M%S)
cp /app/db.sqlite3 /backups/db_backup_$DATE.sqlite3

# Mantener solo últimos 30 backups
find /backups -name "db_backup_*.sqlite3" -mtime +30 -delete
```

### 2. Verificación de Integridad
```python
# manage.py command para verificar BD
from django.core.management.base import BaseCommand
import sqlite3

class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('PRAGMA integrity_check;')
        result = cursor.fetchone()
        self.stdout.write(f"Integridad: {result[0]}")
```

### 3. Optimización Periódica
```sql
-- Ejecutar mensualmente
VACUUM;           -- Reorganiza y compacta la BD
ANALYZE;          -- Actualiza estadísticas para el optimizador
```

## 📈 Monitoreo y Rendimiento

### 1. Métricas Importantes
- **Tamaño del archivo**: `ls -lh db.sqlite3`
- **Tiempo de respuesta**: Logs de Django
- **Bloqueos**: Monitor de queries lentas
- **Uso de memoria**: htop/Task Manager

### 2. Alertas Recomendadas
- BD >500MB (considerar limpieza)
- Queries >1 segundo
- Errores de "database locked"
- Espacio en disco <20%

## 🚨 Cuándo Migrar a PostgreSQL

Considera migrar si experimentas:

1. **Errores frecuentes de "database locked"**
2. **Más de 200 usuarios concurrentes regulares**
3. **BD >1GB con crecimiento continuo**
4. **Necesidad de características avanzadas** (full-text search, JSON, etc.)
5. **Múltiples aplicaciones** accediendo a la misma BD

## 🔄 Plan de Migración (Futuro)

Si necesitas migrar:

### 1. Preparación
```bash
# Backup completo
python manage.py dumpdata > backup.json

# Instalar psycopg2
pip install psycopg2-binary
```

### 2. Nueva Configuración
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'protectora_adan',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Migración
```bash
# Crear nueva BD
python manage.py migrate

# Cargar datos
python manage.py loaddata backup.json
```

## 🛡️ Seguridad

### 1. Permisos de Archivo
```bash
# Solo el usuario de la aplicación debe acceder
chmod 600 db.sqlite3
chown www-data:www-data db.sqlite3
```

### 2. Ubicación Segura
- **Fuera del directorio web** (no accesible por HTTP)
- **En directorio con permisos restringidos**
- **Con backups encriptados**

### 3. Validación Regular
```python
# Verificar corrupción
python manage.py check --database=default
```

## 🎯 Conclusión

SQLite es **perfectamente adecuado** para Protectora Adán porque:

- ✅ Cumple con los requisitos de tráfico esperado
- ✅ Simplifica deployment y mantenimiento
- ✅ Proporciona excelente rendimiento para este caso de uso
- ✅ Permite fácil backup y recuperación
- ✅ Reduce costos operativos

La configuración optimizada implementada asegura el mejor rendimiento posible manteniendo la simplicidad que caracteriza a SQLite.

## 📚 Referencias

- [SQLite When To Use](https://www.sqlite.org/whentouse.html)
- [Django SQLite Notes](https://docs.djangoproject.com/en/4.2/ref/databases/#sqlite-notes)
- [SQLite Performance Tips](https://www.sqlite.org/optoverview.html)
