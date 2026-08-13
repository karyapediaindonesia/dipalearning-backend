import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.branches.models import Holiday

# Delete all API synced holidays
deleted_count, _ = Holiday.objects.filter(notes='Diambil otomatis dari API Sinkronisasi.').delete()
print(f'Deleted {deleted_count} old holidays.')
