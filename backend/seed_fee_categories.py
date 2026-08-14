import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.finance.models import FeeCategory

print("Seeding Fee Categories...")

categories_data = [
    # Parent Categories
    {
        "code": "OPEX",
        "name": "Biaya Operasional",
        "parent_code": None,
        "classification": "OPEX",
        "cost_nature": "PERIODIC",
        "status": "ACTIVE",
    },
    {
        "code": "ACAD",
        "name": "Biaya Akademik",
        "parent_code": None,
        "classification": "ACADEMIC",
        "cost_nature": "VARIABLE",
        "status": "ACTIVE",
    },
    
    # Subcategories - OPEX
    {
        "code": "OPEX-LST",
        "name": "Listrik",
        "parent_code": "OPEX",
        "classification": "OPEX",
        "cost_nature": "PERIODIC",
        "status": "ACTIVE",
    },
    {
        "code": "OPEX-INT",
        "name": "Internet",
        "parent_code": "OPEX",
        "classification": "OPEX",
        "cost_nature": "FIXED",
        "status": "ACTIVE",
    },
    {
        "code": "OPEX-AIR",
        "name": "Air",
        "parent_code": "OPEX",
        "classification": "OPEX",
        "cost_nature": "PERIODIC",
        "status": "ACTIVE",
    },
    {
        "code": "OPEX-KBR",
        "name": "Kebersihan",
        "parent_code": "OPEX",
        "classification": "OPEX",
        "cost_nature": "PERIODIC",
        "status": "ACTIVE",
    },

    # Subcategories - ACADEMIC
    {
        "code": "ACAD-BAH",
        "name": "Bahan Ajar",
        "parent_code": "ACAD",
        "classification": "ACADEMIC",
        "cost_nature": "VARIABLE",
        "status": "ACTIVE",
    },
    {
        "code": "ACAD-TRN",
        "name": "Pelatihan Coach",
        "parent_code": "ACAD",
        "classification": "ACADEMIC",
        "cost_nature": "PERIODIC",
        "status": "ACTIVE",
    },
    {
        "code": "ACAD-STU",
        "name": "Kegiatan Siswa",
        "parent_code": "ACAD",
        "classification": "ACADEMIC",
        "cost_nature": "VARIABLE",
        "status": "ACTIVE",
    }
]

count = 0
for data in categories_data:
    parent = None
    if data['parent_code']:
        parent = FeeCategory.objects.get(code=data['parent_code'])
    
    obj, created = FeeCategory.objects.update_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'parent': parent,
            'classification': data['classification'],
            'cost_nature': data['cost_nature'],
            'status': data['status'],
        }
    )
    if created:
        print(f"Created: {obj.code} - {obj.name}")
    else:
        print(f"Updated: {obj.code} - {obj.name}")
    count += 1

print(f"Successfully seeded {count} fee categories.")
