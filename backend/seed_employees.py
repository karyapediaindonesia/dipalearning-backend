import os, django, random
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.hr.models import Employee, JobPosition, EmployeeBranchAssignment
from apps.branches.models import Branch

# --- Clear existing ---
EmployeeBranchAssignment.objects.all().delete()
Employee.objects.all().delete()
print("Cleared existing employees and assignments.")

positions = {p.name: p for p in JobPosition.objects.all()}
branches  = list(Branch.objects.all())

male_names = [
    "Ahmad Fauzi", "Budi Santoso", "Dian Prasetyo", "Eko Wahyudi", "Fajar Nugroho",
    "Galih Setiawan", "Hendra Kusuma", "Irfan Maulana", "Joko Susanto", "Kevin Pratama",
    "Lukman Hakim", "Muhammad Rizki", "Nanda Firmansyah", "Oscar Hidayat", "Puguh Wibowo",
    "Rahmat Saputra", "Surya Permana", "Tri Cahyono", "Umar Saleh", "Vino Adiputra",
    "Wahyu Saputro", "Yusuf Bahtiar", "Zainal Abidin", "Arif Budiman", "Bagas Dwiyanto",
    "Candra Putra", "Dendi Kurniawan", "Erwin Susanto", "Ferry Gunawan", "Gilang Ramadan",
    "Harry Purnomo", "Ivan Taufik", "Jeffry Kurnia", "Kresna Wicaksono", "Lanang Jati",
    "Marwan Hafidz", "Niko Adyatma", "Okky Ferdiansyah", "Panji Gumelar", "Reza Aditama",
    "Satria Muda", "Taufan Nurhadi", "Udin Supriyadi", "Vicky Andrian", "Wawan Setianto",
    "Yoga Prastowo", "Zaki Ramadhan", "Adam Kuswoyo", "Bagus Pramudia", "Chandra Wiratama",
    "Dani Permadi", "Edho Saputra", "Fendi Hartanto", "Gema Pratama", "Habib Mustofa",
]
female_names = [
    "Ani Rahayu", "Bella Susanti", "Citra Dewi", "Dina Ratnasari", "Eka Putri",
    "Fitri Handayani", "Gita Permata", "Hana Safitri", "Indah Lestari", "Julia Kartika",
    "Kartini Wulandari", "Lina Marlina", "Maya Sari", "Nita Kusumawati", "Okti Rahmawati",
    "Putri Anggraeni", "Rini Setyowati", "Sari Andriani", "Tika Maharani", "Uswatun Khasanah",
    "Vivi Novitasari", "Wida Pratiwi", "Yeni Kurniasih", "Zahra Fauziah", "Amelia Sari",
    "Bunga Puspitasari", "Clara Nindya", "Devi Ayu", "Elsa Kusumawardani", "Fanny Octavia",
    "Grace Puspita", "Helena Darmawan", "Ika Rachmawati", "Juwita Ningrum", "Kania Nur",
    "Layla Syahida", "Mira Anggraini", "Nina Fitriani", "Olivia Susanto", "Priska Anjani",
    "Retno Yulianti", "Siska Aprilia", "Tiara Cahyani", "Ulfa Hardianti", "Virna Dewi",
    "Wulan Kusuma", "Yolanda Putri", "Zara Salsabila", "Adinda Novia", "Berliana Kartika",
    "Cintya Andini", "Desti Ramadhani", "Erinna Putri", "Febriana Sari", "Giska Permata",
]

used_names = []
counter = [1]

def pick_name(gender=None):
    pool = male_names if gender == 'M' else (female_names if gender == 'F' else male_names + female_names)
    remaining = [n for n in pool if n not in used_names]
    if not remaining:
        base = random.choice(pool)
        name = f"{base} {counter[0]}"
        counter[0] += 1
        return name
    name = random.choice(remaining)
    used_names.append(name)
    return name

def random_birth_date():
    year = random.randint(1985, 2000)
    return date(year, random.randint(1, 12), random.randint(1, 28))

def random_join_date():
    year = random.randint(2019, 2024)
    return date(year, random.randint(1, 12), random.randint(1, 28))

idx = 1
total = 0

def create_employee(branch, pos_name, pos_code, gender, emp_type):
    global idx, total
    pos = positions.get(pos_name)
    if not pos:
        print(f"  WARNING: Position '{pos_name}' not found!")
        return
    name = pick_name(gender)
    emp_num = f"EMP-{branch.code}-{pos_code}-{idx:03d}"
    emp = Employee.objects.create(
        employee_number=emp_num,
        full_name=name,
        nickname=name.split()[0],
        gender=gender,
        birth_date=random_birth_date(),
        phone=f"08{random.randint(100000000, 999999999)}",
        employee_type=emp_type,
        join_date=random_join_date(),
        job_position=pos,
        status='ACTIVE',
    )
    # Assign to branch
    EmployeeBranchAssignment.objects.create(
        employee=emp,
        branch=branch,
        role_in_branch=pos.name,
        is_active=True,
    )
    idx += 1
    total += 1
    print(f"  + {emp_num} | {name} | {pos_name} ({emp_type}) @ {branch.name}")

for branch in branches:
    print(f"\n=== {branch.name} ({branch.code}) ===")

    # 1. Management
    create_employee(branch, 'Branch Manager',       'BRM', 'M', 'FULL_TIME')
    create_employee(branch, 'Operational Manager',  'OPM', 'M', 'FULL_TIME')

    # 2. Academic Core
    create_employee(branch, 'Academic Coordinator', 'ACO', 'F', 'FULL_TIME')
    create_employee(branch, 'Academic Admin',       'ACA', 'F', 'FULL_TIME')

    # 3. Admins and Support
    for _ in range(2):
        create_employee(branch, 'Front Admin', 'FRN', 'F', 'FULL_TIME')
    
    create_employee(branch, 'Finance Admin', 'FIN', 'F', 'FULL_TIME')
    create_employee(branch, 'General Affair', 'GA', 'M', 'FULL_TIME')
    create_employee(branch, 'Marketing Officer', 'MKT', 'M', 'FULL_TIME')

    # 4. Coaches
    create_employee(branch, 'Assistant Coach',      'ASC', random.choice(['M','F']), 'FULL_TIME')

    num_coaches = random.randint(15, 25)
    coach_types = ['FULL_TIME', 'FULL_TIME', 'PART_TIME', 'PART_TIME', 'FREELANCE']  # weighted
    for _ in range(num_coaches):
        gender = random.choice(['M', 'F'])
        emp_type = random.choice(coach_types)
        create_employee(branch, 'Coach', 'CHC', gender, emp_type)

print(f"\n{'='*60}")
print(f"SELESAI: {total} pegawai berhasil ditambahkan di {len(branches)} cabang.")
print(f"{'='*60}")
