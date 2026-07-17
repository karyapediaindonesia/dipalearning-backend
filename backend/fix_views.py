import os

path = r"C:\dipalearning\backend\apps\dashboard\views.py"

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Truncate at line 630
new_lines = lines[:630]

appended_code = """
@login_required
def master_metode_bayar(request):
    methods = PaymentMethod.objects.all().order_by('code')
    return render(request, 'dashboard/pages/master-metode-bayar.html', {
        'methods': methods,
        'page_title': 'Master Metode Pembayaran'
    })

@login_required
def master_kategori_biaya(request):
    categories = FeeCategory.objects.select_related('parent').all().order_by('code')
    return render(request, 'dashboard/pages/master-kategori-biaya.html', {
        'categories': categories,
        'page_title': 'Master Kategori Biaya'
    })

from apps.students.models import Prospect, Enrollment, Student
from apps.hr.models import Employee
from apps.academics.models import Package, AcademicPeriod, Course

@login_required
def registrasi_siswa(request):
    prospects = Prospect.objects.all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/registrasi-siswa.html', {
        'prospects': prospects,
        'branches': branches,
        'page_title': 'Registrasi Calon Siswa'
    })

@login_required
def enrollment_siswa(request):
    prospects = Prospect.objects.filter(status='REGISTERED')
    enrollments = Enrollment.objects.all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    packages = Package.objects.filter(status='ACTIVE')
    periods = AcademicPeriod.objects.exclude(status='ARCHIVED')
    coaches = Employee.objects.filter(job_title__icontains='Coach', status='ACTIVE')
    
    return render(request, 'dashboard/pages/enrollment-siswa.html', {
        'prospects': prospects,
        'enrollments': enrollments,
        'branches': branches,
        'courses': courses,
        'packages': packages,
        'periods': periods,
        'coaches': coaches,
        'page_title': 'Enrollment Siswa'
    })

@login_required
def master_karyawan(request):
    employees = Employee.objects.all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/master-karyawan.html', {
        'employees': employees,
        'branches': branches,
        'courses': courses,
        'page_title': 'Master Karyawan'
    })
"""

new_lines.append(appended_code)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("views.py fixed successfully.")
