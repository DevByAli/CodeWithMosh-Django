import os
from pathlib import Path
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        
        sql = Path(file_path).read_text()
        
        with connection.cursor() as cursor:
            cursor.execute(sql)