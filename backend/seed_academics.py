import os, django
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.academics.models import AcademicYear, AcademicPeriod, Package, Level, Course

print("Seeding Academic Years and Periods...")

# 1. Academic Year & Periods
ay_26, _ = AcademicYear.objects.get_or_create(
    code='AY2627',
    defaults={
        'name': '2026/2027',
        'start_year': 2026,
        'end_year': 2027,
        'status': 'ACTIVE'
    }
)
ay_27, _ = AcademicYear.objects.get_or_create(
    code='AY2728',
    defaults={
        'name': '2027/2028',
        'start_year': 2027,
        'end_year': 2028,
        'status': 'INACTIVE'
    }
)

# Academic Periods for AY2627
p1, _ = AcademicPeriod.objects.get_or_create(
    code='SEM1-2627',
    defaults={
        'academic_year': ay_26,
        'name': 'Semester Ganjil 26/27',
        'period_type': 'SEMESTER',
        'sequence': 1,
        'start_date': date(2026, 7, 1),
        'end_date': date(2026, 12, 31),
        'registration_start': date(2026, 5, 1),
        'registration_end': date(2026, 7, 31),
        'learning_start': date(2026, 7, 15),
        'learning_end': date(2026, 12, 20),
    }
)
p2, _ = AcademicPeriod.objects.get_or_create(
    code='SEM2-2627',
    defaults={
        'academic_year': ay_26,
        'name': 'Semester Genap 26/27',
        'period_type': 'SEMESTER',
        'sequence': 2,
        'start_date': date(2027, 1, 1),
        'end_date': date(2027, 6, 30),
        'registration_start': date(2026, 11, 1),
        'registration_end': date(2027, 1, 31),
        'learning_start': date(2027, 1, 15),
        'learning_end': date(2027, 6, 20),
    }
)
p3, _ = AcademicPeriod.objects.get_or_create(
    code='TERM1-2627',
    defaults={
        'academic_year': ay_26,
        'name': 'Term 1 26/27',
        'period_type': 'TERM',
        'sequence': 1,
        'start_date': date(2026, 7, 1),
        'end_date': date(2026, 9, 30)
    }
)

print("Seeding Education Packages...")

# We need combinations of levels.
levels_smp = list(Level.objects.filter(course__code='SMP'))
levels_bts = list(Level.objects.filter(course__code='BTS'))
levels_elm = list(Level.objects.filter(course__code='ELM'))
levels_ele = list(Level.objects.filter(course__code='ELE'))
levels_sme = list(Level.objects.filter(course__code='SME'))
levels_rba = list(Level.objects.filter(course__code='RBA'))

# Package 1: Sempoa SIP - Paket 4 Bulan (40x Pertemuan) - All Levels of SMP
pkg1, _ = Package.objects.get_or_create(
    name='Paket Sempoa SIP 4 Bulan',
    defaults={
        'price': 1500000.00,
        'meetings_quota': 40,
        'validity_days': 120,
        'notes': 'Paket intensif 4 bulan untuk semua level Sempoa SIP.'
    }
)
pkg1.levels.set(levels_smp)

# Package 2: BUNDLE Eye Level (Math + English) - Semester
# Combination of multiple programs (Math and English)
pkg2, _ = Package.objects.get_or_create(
    name='Bundling Eye Level (Math + English) 6 Bulan',
    defaults={
        'price': 4500000.00,
        'meetings_quota': 48, # 24 Math, 24 English
        'validity_days': 180,
        'notes': 'Harga spesial bundling Math dan English (Basic & Critical Thinking Math, Lower & Higher English).'
    }
)
pkg2.levels.set(levels_elm + levels_ele)

# Package 3: Paket Bahasa Inggris Hemat (Smarter English Junior + Foundation)
pkg3, _ = Package.objects.get_or_create(
    name='Paket Smarter English Junior & Foundation (3 Bulan)',
    defaults={
        'price': 1200000.00,
        'meetings_quota': 24,
        'validity_days': 90,
        'notes': 'Dapat digunakan untuk level Foundation atau Junior.'
    }
)
pkg3.levels.set(levels_sme)

# Package 4: BUNDLE Kreatif (Baca Tulis + Rainbow Art)
pkg4, _ = Package.objects.get_or_create(
    name='Paket Kreatif Pra-Sekolah (BTS + Rainbow Art)',
    defaults={
        'price': 2000000.00,
        'meetings_quota': 30, # 15 BTS, 15 Art
        'validity_days': 90,
        'notes': 'Kombinasi program Baca Tulis SIP dan Rainbow Art (Semua Level).'
    }
)
pkg4.levels.set(levels_bts + levels_rba)

# Package 5: Paket Combo ALL-IN (Semua Kursus yang ada!)
pkg5, _ = Package.objects.get_or_create(
    name='VIP Combo All-In-One (1 Tahun)',
    defaults={
        'price': 15000000.00,
        'meetings_quota': 250,
        'validity_days': 365,
        'notes': 'Member VIP: Bebas ikut program apa saja (semua level, semua kursus) selama 1 tahun.'
    }
)
pkg5.levels.set(list(Level.objects.all()))

print(f"Successfully seeded {AcademicYear.objects.count()} Academic Years.")
print(f"Successfully seeded {AcademicPeriod.objects.count()} Academic Periods.")
print(f"Successfully seeded {Package.objects.count()} Education Packages.")
