import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.branches.models import Branch, Holiday
import requests

data = requests.get('https://date.nager.at/api/v3/PublicHolidays/2026/ID').json()
branch = Branch.objects.filter(is_active=True).first()

if branch:
    print(f'Starting sync for branch: {branch.name}')
    created_count = 0
    for item in data:
        date_str = item.get('date')
        name = item.get('localName') or item.get('name')
        
        Holiday.objects.update_or_create(
            branch=branch,
            date_start=date_str,
            name=name,
            defaults={
                'date_end': date_str,
                'holiday_type': 'NATIONAL',
                'operational_impact': 'FULL_CLOSE',
                'status': 'ACTIVE',
                'notes': 'Diambil otomatis dari API Sinkronisasi.'
            }
        )
        created_count += 1
    
    print(f'Successfully created/updated {created_count} holidays.')
else:
    print('No active branch found!')

print(f'Total Holidays in DB: {Holiday.objects.count()}')
