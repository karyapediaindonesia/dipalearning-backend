import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.branches.models import Branch, Room

Room.objects.all().delete()

branches = Branch.objects.all()
count = 0

for branch in branches:
    # 2-3 floors simulation
    rooms_data = [
        # Floor 1
        {"code": f"{branch.code}-101", "name": "Ruang Kelas 101 (Lantai 1)", "room_type": "CLASSROOM", "cap_ideal": 20, "cap_max": 25, "fac": ["AC", "Proyektor", "Papan Tulis"]},
        {"code": f"{branch.code}-102", "name": "Ruang Kelas 102 (Lantai 1)", "room_type": "CLASSROOM", "cap_ideal": 20, "cap_max": 25, "fac": ["AC", "Proyektor", "Papan Tulis"]},
        {"code": f"{branch.code}-103", "name": "Ruang Administrasi (Lantai 1)", "room_type": "ADMINISTRATION", "cap_ideal": 5, "cap_max": 10, "fac": ["AC", "Komputer", "Printer", "CCTV"]},
        
        # Floor 2
        {"code": f"{branch.code}-201", "name": "Ruang Privat 201 (Lantai 2)", "room_type": "PRIVATE", "cap_ideal": 4, "cap_max": 6, "fac": ["AC", "Smart TV", "Papan Tulis Kaca"]},
        {"code": f"{branch.code}-202", "name": "Ruang Kelompok 202 (Lantai 2)", "room_type": "GROUP", "cap_ideal": 10, "cap_max": 15, "fac": ["AC", "Proyektor", "Meja Bundar diskusi"]},
        {"code": f"{branch.code}-203", "name": "Lab Komputer (Lantai 2)", "room_type": "LABORATORY", "cap_ideal": 15, "cap_max": 20, "fac": ["AC", "15 PC Core i7", "Server Lokal"]},
        
        # Floor 3
        {"code": f"{branch.code}-301", "name": "Ruang Rapat Utama (Lantai 3)", "room_type": "MEETING", "cap_ideal": 10, "cap_max": 15, "fac": ["AC", "Proyektor", "Sound System", "Video Conference"]},
        {"code": f"{branch.code}-302", "name": "Aula Serbaguna (Lantai 3)", "room_type": "HALL", "cap_ideal": 50, "cap_max": 100, "fac": ["AC Sentral", "Panggung Mini", "Sound System Besar"]},
    ]
    
    for r_data in rooms_data:
        Room.objects.create(
            branch=branch,
            code=r_data["code"],
            name=r_data["name"],
            room_type=r_data["room_type"],
            capacity_ideal=r_data["cap_ideal"],
            capacity_max=r_data["cap_max"],
            facilities=r_data["fac"],
            status="ACTIVE"
        )
        count += 1
        
print(f"Successfully seeded {count} rooms across {branches.count()} branches!")
