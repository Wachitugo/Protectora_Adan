#!/usr/bin/env python
"""
Script de mantenimiento para SQLite
Ejecutar periódicamente para mantener la base de datos optimizada
"""
import os
import sys
import sqlite3
import shutil
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'protectora_adan.settings')
import django
django.setup()

from django.conf import settings

def get_db_path():
    """Obtener la ruta de la base de datos SQLite"""
    db_config = settings.DATABASES['default']
    if 'sqlite' in db_config['ENGINE']:
        return db_config['NAME']
    else:
        print("❌ Esta aplicación no está configurada para usar SQLite")
        sys.exit(1)

def backup_database(db_path):
    """Crear backup de la base de datos"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.path.dirname(db_path), 'backups')
    
    # Crear directorio de backups si no existe
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_path = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        
        # Limpiar backups antiguos (mantener últimos 10)
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('db_backup_')])
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(os.path.join(backup_dir, old_backup))
                print(f"🗑️  Backup antiguo eliminado: {old_backup}")
                
        return backup_path
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return None

def check_integrity(db_path):
    """Verificar integridad de la base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando integridad de la base de datos...")
        cursor.execute('PRAGMA integrity_check;')
        result = cursor.fetchone()
        
        if result[0] == 'ok':
            print("✅ Integridad: OK")
        else:
            print(f"❌ Problema de integridad: {result[0]}")
            
        conn.close()
        return result[0] == 'ok'
    except Exception as e:
        print(f"❌ Error verificando integridad: {e}")
        return False

def optimize_database(db_path):
    """Optimizar la base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("⚡ Optimizando base de datos...")
        
        # Obtener tamaño antes
        size_before = os.path.getsize(db_path)
        
        # VACUUM para reorganizar y compactar
        print("  📦 Ejecutando VACUUM...")
        cursor.execute('VACUUM;')
        
        # ANALYZE para actualizar estadísticas
        print("  📊 Ejecutando ANALYZE...")
        cursor.execute('ANALYZE;')
        
        # Obtener tamaño después
        size_after = os.path.getsize(db_path)
        
        conn.close()
        
        # Mostrar resultados
        size_diff = size_before - size_after
        if size_diff > 0:
            print(f"✅ Optimización completada. Espacio liberado: {size_diff:,} bytes")
        else:
            print("✅ Optimización completada. Base de datos ya estaba optimizada.")
            
        return True
    except Exception as e:
        print(f"❌ Error optimizando: {e}")
        return False

def show_stats(db_path):
    """Mostrar estadísticas de la base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n📊 Estadísticas de la base de datos:")
        print("-" * 40)
        
        # Tamaño del archivo
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"📁 Tamaño del archivo: {size_mb:.2f} MB")
        
        # Número de tablas
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
        table_count = cursor.fetchone()[0]
        print(f"🗂️  Número de tablas: {table_count}")
        
        # Configuración actual
        pragmas = [
            'journal_mode', 'synchronous', 'cache_size', 
            'temp_store', 'mmap_size', 'foreign_keys'
        ]
        
        print("\n⚙️ Configuración actual:")
        for pragma in pragmas:
            cursor.execute(f'PRAGMA {pragma};')
            value = cursor.fetchone()[0]
            print(f"  {pragma}: {value}")
        
        # Estadísticas de tablas principales
        tables = ['core_perro', 'donaciones_donacion', 'adopciones_solicitudadopcion']
        print("\n📋 Registros por tabla:")
        for table in tables:
            try:
                cursor.execute(f"SELECT count(*) FROM {table};")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,}")
            except sqlite3.OperationalError:
                # Tabla no existe
                pass
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal"""
    print("🗄️ SQLite Maintenance Tool - Protectora Adán")
    print("=" * 50)
    
    db_path = get_db_path()
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        sys.exit(1)
    
    print(f"📂 Base de datos: {db_path}")
    
    # Mostrar estadísticas
    show_stats(db_path)
    
    # Verificar integridad
    if not check_integrity(db_path):
        print("❌ Problemas de integridad detectados. No se procederá con la optimización.")
        sys.exit(1)
    
    # Crear backup
    backup_path = backup_database(db_path)
    if not backup_path:
        print("❌ No se pudo crear backup. Abortando.")
        sys.exit(1)
    
    # Optimizar
    if optimize_database(db_path):
        print("\n✅ Mantenimiento completado exitosamente")
    else:
        print("\n❌ Error durante el mantenimiento")
        # Restaurar backup si hay error
        print("🔄 Restaurando backup...")
        shutil.copy2(backup_path, db_path)
        print("✅ Backup restaurado")

if __name__ == "__main__":
    main()
