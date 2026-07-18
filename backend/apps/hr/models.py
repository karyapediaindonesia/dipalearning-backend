from django.db import models
from apps.core.models import SoftDeleteModel

class JobPosition(SoftDeleteModel):
    CATEGORY_CHOICES = [
        ('MANAGEMENT', 'Management'),
        ('ACADEMIC', 'Academic'),
        ('SALES', 'Sales & Marketing'),
        ('FINANCE', 'Finance & Admin'),
        ('SUPPORT', 'Support & Ops'),
        ('OTHER', 'Lainnya')
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name='Kode Jabatan')
    name = models.CharField(max_length=100, verbose_name='Nama Jabatan')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    parent_position = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    level = models.PositiveIntegerField(default=1, help_text="Tingkat jabatan (1 = tertinggi)")
    
    # Flags untuk logic aplikasi
    is_teaching_position = models.BooleanField(default=False, help_text="Centang jika jabatan ini mengajar (Coach)")
    is_finance_validator = models.BooleanField(default=False, help_text="Bisa memvalidasi pembayaran")
    requires_schedule = models.BooleanField(default=False)
    requires_attendance = models.BooleanField(default=False)
    requires_payroll = models.BooleanField(default=True)
    
    status = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        db_table = 'job_positions'

    def __str__(self):
        return f"{self.code} - {self.name}"

class Employee(SoftDeleteModel):
    GENDER_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    EMP_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('FREELANCE', 'Freelance'),
        ('INTERN', 'Intern')
    ]
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('LEAVE', 'Leave'),
        ('SUSPENDED', 'Suspended'),
        ('RESIGNED', 'Resigned'),
        ('TERMINATED', 'Terminated')
    ]

    user = models.OneToOneField('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    employee_number = models.CharField(max_length=50, unique=True, verbose_name='Nomor Karyawan')
    full_name = models.CharField(max_length=100, verbose_name='Nama Lengkap')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nama Panggilan')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nik = models.CharField(max_length=50, blank=True, null=True, verbose_name='NIK KTP')
    npwp = models.CharField(max_length=50, blank=True, null=True, verbose_name='NPWP')
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)

    # Contacts
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='No HP')
    whatsapp = models.CharField(max_length=50, blank=True, null=True, verbose_name='WhatsApp')
    personal_email = models.EmailField(blank=True, null=True)
    work_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Kepegawaian & Jabatan
    employee_type = models.CharField(max_length=20, choices=EMP_TYPE_CHOICES, default='FULL_TIME')
    join_date = models.DateField(blank=True, null=True)
    resign_date = models.DateField(blank=True, null=True)
    job_position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Jabatan', related_name='employees')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Departemen')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.employee_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.employee_number:
            count = Employee.objects.count() + 1
            self.employee_number = f"EMP-2026-{count:04d}"
        super().save(*args, **kwargs)


class EmployeeBranchAssignment(SoftDeleteModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='branch_assignments')
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
    role_in_branch = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'employee_branch_assignments'
        unique_together = ('employee', 'branch')

class CoachProfile(SoftDeleteModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='coach_profile')
    specialization = models.CharField(max_length=255, blank=True, null=True, help_text="Contoh: English, Math")
    teaching_level = models.CharField(max_length=255, blank=True, null=True, help_text="Contoh: Beginner - Advanced")
    certification = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    is_active_teaching = models.BooleanField(default=True)

    class Meta:
        db_table = 'coach_profiles'

class EmployeeDocument(SoftDeleteModel):
    DOC_TYPES = [
        ('KTP', 'KTP'), ('KK', 'Kartu Keluarga'), ('IJAZAH', 'Ijazah'), 
        ('SERTIFIKAT', 'Sertifikat'), ('KONTRAK', 'Kontrak Kerja'), ('NPWP', 'NPWP'), ('LAINNYA', 'Lainnya')
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOC_TYPES)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'employee_documents'

class EmployeeHistory(SoftDeleteModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='histories')
    change_type = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'employee_histories'
