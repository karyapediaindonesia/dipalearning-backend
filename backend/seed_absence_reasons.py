import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.attendance.models import AbsenceReason

print("Seeding Absence Reasons...")

reasons_data = [
    {
        "code": "SKT",
        "name": "Sakit",
        "applies_to": "BOTH",
        "classification": "EXCUSED",
        "is_makeup_eligible": "ELIGIBLE",
        "status": "ACTIVE",
        "notes": "Tidak hadir karena sakit (memerlukan surat dokter jika lebih dari 2 hari)."
    },
    {
        "code": "IZN",
        "name": "Izin",
        "applies_to": "BOTH",
        "classification": "EXCUSED",
        "is_makeup_eligible": "ELIGIBLE",
        "status": "ACTIVE",
        "notes": "Tidak hadir karena urusan pribadi/keluarga."
    },
    {
        "code": "ALP",
        "name": "Alpha / Tanpa Keterangan",
        "applies_to": "BOTH",
        "classification": "UNEXCUSED",
        "is_makeup_eligible": "NOT_ELIGIBLE",
        "status": "ACTIVE",
        "notes": "Tidak hadir tanpa pemberitahuan sama sekali."
    },
    {
        "code": "CUTI",
        "name": "Cuti Tahunan",
        "applies_to": "COACH",
        "classification": "EXCUSED",
        "is_makeup_eligible": "REQUIRES_APPROVAL",
        "status": "ACTIVE",
        "notes": "Pengajuan cuti tahunan (khusus karyawan/coach)."
    },
    {
        "code": "TGS",
        "name": "Tugas Luar / Dinas",
        "applies_to": "COACH",
        "classification": "EXCUSED",
        "is_makeup_eligible": "REQUIRES_APPROVAL",
        "status": "ACTIVE",
        "notes": "Ditugaskan ke luar kantor/cabang lain."
    },
    {
        "code": "LBR",
        "name": "Libur Nasional",
        "applies_to": "BOTH",
        "classification": "EXCUSED",
        "is_makeup_eligible": "NOT_ELIGIBLE",
        "status": "ACTIVE",
        "notes": "Hari libur resmi."
    }
]

count = 0
for data in reasons_data:
    obj, created = AbsenceReason.objects.update_or_create(
        code=data['code'],
        defaults=data
    )
    if created:
        print(f"Created: {obj.code} - {obj.name}")
    else:
        print(f"Updated: {obj.code} - {obj.name}")
    count += 1

print(f"Successfully seeded {count} absence reasons.")
