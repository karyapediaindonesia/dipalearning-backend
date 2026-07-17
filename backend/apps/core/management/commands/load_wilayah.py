import requests
from django.core.management.base import BaseCommand
from apps.core.models import Province, City

class Command(BaseCommand):
    help = 'Load Provinces and Cities from EMSIFA API'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Fetching Provinces...'))
        try:
            prov_res = requests.get('https://emsifa.github.io/api-wilayah-indonesia/api/provinces.json')
            prov_res.raise_for_status()
            provinces = prov_res.json()
            
            created_prov = 0
            for p in provinces:
                Province.objects.update_or_create(
                    id=p['id'],
                    defaults={'name': p['name']}
                )
                created_prov += 1
                
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_prov} provinces.'))
            
            self.stdout.write(self.style.WARNING('Fetching Cities...'))
            created_city = 0
            for p in provinces:
                city_res = requests.get(f'https://emsifa.github.io/api-wilayah-indonesia/api/regencies/{p["id"]}.json')
                if city_res.status_code == 200:
                    cities = city_res.json()
                    for c in cities:
                        City.objects.update_or_create(
                            id=c['id'],
                            defaults={
                                'province_id': c['province_id'],
                                'name': c['name']
                            }
                        )
                        created_city += 1
                        
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {created_city} cities.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to load data: {e}'))
