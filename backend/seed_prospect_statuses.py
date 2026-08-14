import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.students.models import ProspectStatus

print("Seeding Prospect Statuses...")

statuses_data = [
    {
        "code": "NEW",
        "name": "Prospek Baru",
        "sequence": 1,
        "description": "Data baru masuk dan belum dilakukan tindakan.",
        "is_initial": True,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 10,
        "color": "primary",
        "status": True,
    },
    {
        "code": "CONTACTED",
        "name": "Sudah Dihubungi",
        "sequence": 2,
        "description": "Admin sudah melakukan kontak pertama.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 20,
        "color": "info",
        "status": True,
    },
    {
        "code": "INTERESTED",
        "name": "Berminat",
        "sequence": 3,
        "description": "Calon siswa menunjukkan ketertarikan.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 40,
        "color": "info",
        "status": True,
    },
    {
        "code": "CONSULTATION",
        "name": "Konsultasi",
        "sequence": 4,
        "description": "Sudah berdiskusi lebih detail.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 50,
        "color": "warning",
        "status": True,
    },
    {
        "code": "ASSESSMENT",
        "name": "Assessment",
        "sequence": 5,
        "description": "Calon siswa sedang mengikuti atau sudah dijadwalkan assessment.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 60,
        "color": "warning",
        "status": True,
    },
    {
        "code": "TRIAL",
        "name": "Trial Class",
        "sequence": 6,
        "description": "Calon siswa mengikuti kelas percobaan.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 70,
        "color": "warning",
        "status": True,
    },
    {
        "code": "OFFERED",
        "name": "Penawaran Diberikan",
        "sequence": 7,
        "description": "Program/paket/harga sudah diberikan.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 80,
        "color": "secondary",
        "status": True,
    },
    {
        "code": "WAITING_DECISION",
        "name": "Menunggu Keputusan",
        "sequence": 8,
        "description": "Orang tua belum menentukan lanjut/tidak.",
        "is_initial": False,
        "is_success": False,
        "is_failed": False,
        "allow_conversion": False,
        "requires_followup": True,
        "probability": 85,
        "color": "secondary",
        "status": True,
    },
    {
        "code": "CONVERTED",
        "name": "Berhasil Menjadi Siswa",
        "sequence": 9,
        "description": "Prospek berhasil dikonversi menjadi siswa.",
        "is_initial": False,
        "is_success": True,
        "is_failed": False,
        "allow_conversion": True,
        "requires_followup": False,
        "probability": 100,
        "color": "success",
        "status": True,
    },
    {
        "code": "LOST",
        "name": "Tidak Berhasil",
        "sequence": 10,
        "description": "Calon siswa tidak jadi bergabung.",
        "is_initial": False,
        "is_success": False,
        "is_failed": True,
        "allow_conversion": False,
        "requires_followup": False,
        "probability": 0,
        "color": "danger",
        "status": True,
    },
    {
        "code": "INVALID",
        "name": "Data Tidak Valid",
        "sequence": 11,
        "description": "Data tidak dapat diproses (Duplikat, form palsu, dsb).",
        "is_initial": False,
        "is_success": False,
        "is_failed": True,
        "allow_conversion": False,
        "requires_followup": False,
        "probability": 0,
        "color": "dark",
        "status": True,
    }
]

count = 0
for data in statuses_data:
    obj, created = ProspectStatus.objects.update_or_create(
        code=data['code'],
        defaults=data
    )
    if created:
        print(f"Created: {obj.code} - {obj.name}")
    else:
        print(f"Updated: {obj.code} - {obj.name}")
    count += 1

print(f"Successfully seeded {count} prospect statuses.")
