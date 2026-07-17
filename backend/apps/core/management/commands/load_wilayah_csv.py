import csv
from django.core.management.base import BaseCommand
from apps.core.models import Province, City
from django.db import transaction
import os

class Command(BaseCommand):
    help = 'Load Provinces and Cities from CSV'

    def handle(self, *args, **kwargs):
        csv_path = '/app/data_provinsi_kabupaten_kota_indonesia.csv'
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'File {csv_path} not found.'))
            return

        with transaction.atomic():
            self.stdout.write('Clearing existing Province and City data...')
            City.objects.all().delete()
            Province.objects.all().delete()

            self.stdout.write('Reading CSV...')
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header (Provinsi, Jenis, Nama_Daerah)

                province_dict = {}
                prov_id_counter = 1
                city_id_counter = 1

                for row in reader:
                    if not row or len(row) < 3:
                        continue
                    
                    prov_name = row[0].strip()
                    jenis = row[1].strip()
                    daerah_name = row[2].strip()

                    if jenis.lower() == 'kota administrasi':
                        jenis = 'Kota'
                    elif jenis.lower() == 'kabupaten administrasi':
                        jenis = 'Kabupaten'
                    
                    city_name = f"{jenis} {daerah_name}"
                    
                    if prov_name not in province_dict:
                        prov_id_str = str(prov_id_counter)
                        prov_obj = Province.objects.create(id=prov_id_str, name=prov_name)
                        province_dict[prov_name] = prov_obj
                        prov_id_counter += 1
                    else:
                        prov_obj = province_dict[prov_name]

                    city_id_str = str(city_id_counter)
                    City.objects.create(id=city_id_str, province=prov_obj, name=city_name)
                    city_id_counter += 1

            self.stdout.write(self.style.SUCCESS('Successfully loaded Provinces and Cities from CSV!'))
