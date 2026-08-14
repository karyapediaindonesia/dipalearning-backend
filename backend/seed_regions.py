import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.core.models import Province, City

print("Seeding Provinces and Cities...")

regions = {
    "31": {"name": "DKI Jakarta", "cities": ["3171|Kota Jakarta Pusat", "3172|Kota Jakarta Utara", "3173|Kota Jakarta Barat", "3174|Kota Jakarta Selatan", "3175|Kota Jakarta Timur"]},
    "32": {"name": "Jawa Barat", "cities": ["3273|Kota Bandung", "3271|Kota Bogor", "3275|Kota Bekasi", "3276|Kota Depok", "3204|Kabupaten Bandung", "3201|Kabupaten Bogor"]},
    "33": {"name": "Jawa Tengah", "cities": ["3374|Kota Semarang", "3372|Kota Surakarta", "3371|Kota Magelang", "3308|Kabupaten Magelang", "3309|Kabupaten Boyolali"]},
    "34": {"name": "DI Yogyakarta", "cities": ["3471|Kota Yogyakarta", "3404|Kabupaten Sleman", "3402|Kabupaten Bantul", "3403|Kabupaten Gunungkidul"]},
    "35": {"name": "Jawa Timur", "cities": ["3578|Kota Surabaya", "3573|Kota Malang", "3507|Kabupaten Malang", "3515|Kabupaten Sidoarjo", "3571|Kota Kediri"]},
    "36": {"name": "Banten", "cities": ["3671|Kota Tangerang", "3674|Kota Tangerang Selatan", "3673|Kota Serang"]},
    "51": {"name": "Bali", "cities": ["5171|Kota Denpasar", "5103|Kabupaten Badung", "5104|Kabupaten Gianyar"]},
    "11": {"name": "Aceh", "cities": ["1171|Kota Banda Aceh"]},
    "12": {"name": "Sumatera Utara", "cities": ["1271|Kota Medan"]},
    "13": {"name": "Sumatera Barat", "cities": ["1371|Kota Padang"]},
    "14": {"name": "Riau", "cities": ["1471|Kota Pekanbaru"]},
    "16": {"name": "Sumatera Selatan", "cities": ["1671|Kota Palembang"]},
    "64": {"name": "Kalimantan Timur", "cities": ["6471|Kota Balikpapan", "6472|Kota Samarinda"]},
    "73": {"name": "Sulawesi Selatan", "cities": ["7371|Kota Makassar"]},
}

for prov_id, prov_data in regions.items():
    prov, _ = Province.objects.get_or_create(id=prov_id, defaults={'name': prov_data['name']})
    for city_str in prov_data['cities']:
        city_id, city_name = city_str.split('|')
        City.objects.get_or_create(id=city_id, defaults={'province': prov, 'name': city_name})

print(f"Total Provinces: {Province.objects.count()}")
print(f"Total Cities: {City.objects.count()}")
