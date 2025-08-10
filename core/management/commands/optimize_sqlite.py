from django.core.management.base import BaseCommand
import sqlite3
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Optimiza la base de datos SQLite aplicando PRAGMAs recomendados'

    def handle(self, *args, **options):
        db_config = settings.DATABASES['default']
        
        if 'sqlite' not in db_config['ENGINE']:
            self.stdout.write(
                self.style.ERROR('Este comando solo funciona con SQLite')
            )
            return
        
        db_path = db_config['NAME']
        
        if not os.path.exists(db_path):
            self.stdout.write(
                self.style.ERROR(f'Base de datos no encontrada: {db_path}')
            )
            return
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            self.stdout.write('Aplicando optimizaciones SQLite...')
            
            # Aplicar PRAGMAs de optimización
            optimizations = [
                ('foreign_keys', 'ON'),
                ('journal_mode', 'WAL'),
                ('synchronous', 'NORMAL'),
                ('temp_store', 'MEMORY'),
                ('cache_size', '8000'),
                ('mmap_size', '268435456'),
            ]
            
            for pragma, value in optimizations:
                cursor.execute(f'PRAGMA {pragma} = {value};')
                self.stdout.write(f'  ✓ {pragma} = {value}')
            
            # Ejecutar VACUUM y ANALYZE
            self.stdout.write('Optimizando estructura...')
            cursor.execute('VACUUM;')
            self.stdout.write('  ✓ VACUUM ejecutado')
            
            cursor.execute('ANALYZE;')
            self.stdout.write('  ✓ ANALYZE ejecutado')
            
            conn.close()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Base de datos SQLite optimizada exitosamente')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error optimizando la base de datos: {e}')
            )
