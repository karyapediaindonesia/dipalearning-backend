import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.hr.models import JobPosition

print("Seeding Job Positions...")

positions_data = [
    {
        "code": "OWNER",
        "name": "Owner / Director",
        "category": "MANAGEMENT",
        "level": 1,
        "parent_code": None,
        "is_teaching_position": False,
        "is_finance_validator": True,
        "requires_schedule": False,
        "requires_attendance": False,
    },
    {
        "code": "OP-MGR",
        "name": "Operational Manager",
        "category": "MANAGEMENT",
        "level": 2,
        "parent_code": "OWNER",
        "is_teaching_position": False,
        "is_finance_validator": True,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "BM",
        "name": "Branch Manager",
        "category": "MANAGEMENT",
        "level": 3,
        "parent_code": "OP-MGR",
        "is_teaching_position": False,
        "is_finance_validator": True,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "ACAD-COORD",
        "name": "Academic Coordinator",
        "category": "ACADEMIC",
        "level": 4,
        "parent_code": "BM",
        "is_teaching_position": True,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "ACAD-ADM",
        "name": "Academic Admin",
        "category": "ACADEMIC",
        "level": 5,
        "parent_code": "ACAD-COORD",
        "is_teaching_position": False,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "FRONT-ADM",
        "name": "Front Admin",
        "category": "SUPPORT",
        "level": 5,
        "parent_code": "BM",
        "is_teaching_position": False,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "FIN-ADM",
        "name": "Finance Admin",
        "category": "FINANCE",
        "level": 5,
        "parent_code": "BM",
        "is_teaching_position": False,
        "is_finance_validator": True,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "MKT-OFF",
        "name": "Marketing Officer",
        "category": "SALES",
        "level": 5,
        "parent_code": "BM",
        "is_teaching_position": False,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "COACH",
        "name": "Coach",
        "category": "ACADEMIC",
        "level": 6,
        "parent_code": "ACAD-COORD",
        "is_teaching_position": True,
        "is_finance_validator": False,
        "requires_schedule": True,
        "requires_attendance": True,
    },
    {
        "code": "ASST-COACH",
        "name": "Assistant Coach",
        "category": "ACADEMIC",
        "level": 7,
        "parent_code": "COACH",
        "is_teaching_position": True,
        "is_finance_validator": False,
        "requires_schedule": True,
        "requires_attendance": True,
    },
    {
        "code": "IT-SUPP",
        "name": "IT Support",
        "category": "SUPPORT",
        "level": 5,
        "parent_code": "OP-MGR",
        "is_teaching_position": False,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    },
    {
        "code": "GA",
        "name": "General Affair",
        "category": "SUPPORT",
        "level": 5,
        "parent_code": "BM",
        "is_teaching_position": False,
        "is_finance_validator": False,
        "requires_schedule": False,
        "requires_attendance": True,
    }
]

count = 0
for data in positions_data:
    parent = None
    if data['parent_code']:
        parent = JobPosition.objects.get(code=data['parent_code'])
    
    obj, created = JobPosition.objects.update_or_create(
        code=data['code'],
        defaults={
            'name': data['name'],
            'category': data['category'],
            'level': data['level'],
            'parent_position': parent,
            'is_teaching_position': data['is_teaching_position'],
            'is_finance_validator': data['is_finance_validator'],
            'requires_schedule': data['requires_schedule'],
            'requires_attendance': data['requires_attendance'],
            'status': True,
        }
    )
    if created:
        print(f"Created: {obj.code} - {obj.name}")
    else:
        print(f"Updated: {obj.code} - {obj.name}")
    count += 1

print(f"Successfully seeded {count} job positions.")
