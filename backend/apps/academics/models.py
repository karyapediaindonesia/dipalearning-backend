
from django.db import models
from apps.core.models import SoftDeleteModel

class Course(SoftDeleteModel):
    """
    Menyimpan data Program Utama / Kursus yang ditawarkan oleh institusi.
    
    Relasi Database:
    - Digunakan luas di `Level`, `StudyClass`, `ProspectInterest`, dan `Enrollment`.
    
    Efek Penghapusan (Cascade Behavior):
    - Jika Course dihapus (Hard Delete):
      -> Semua `Level` (Tingkatan) di dalam kursus ini TERHAPUS (CASCADE).
      -> Semua `StudyClass` (Kelas) yang mengajarkan kursus ini TERHAPUS (CASCADE).
      -> Semua `Enrollment` (Pendaftaran siswa) untuk kursus ini TERHAPUS (CASCADE).
      -> Minat calon siswa (`ProspectInterest`) menjadi NULL (SET_NULL).
    """
    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Akademik'),
        ('LANGUAGE', 'Bahasa'),
        ('TECHNOLOGY', 'Teknologi'),
        ('CREATIVITY', 'Kreativitas'),
        ('PRESCHOOL', 'Persiapan sekolah'),
        ('SELF_DEV', 'Pengembangan diri'),
        ('SPECIAL', 'Program khusus'),
    ]

    LEARNING_TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('GROUP', 'Kelompok'),
        ('BOTH', 'Individual dan kelompok'),
    ]
    
    LEARNING_MODE_CHOICES = [
        ('OFFLINE', 'Tatap muka'),
        ('ONLINE', 'Online'),
        ('HYBRID', 'Hybrid'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name='Kode Kursus')
    name = models.CharField(max_length=100, verbose_name='Nama Kursus')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Kategori Kursus')
    learning_type = models.CharField(max_length=20, choices=LEARNING_TYPE_CHOICES, verbose_name='Tipe Pembelajaran')
    learning_mode = models.CharField(max_length=20, choices=LEARNING_MODE_CHOICES, verbose_name='Mode Pembelajaran')
    default_duration = models.PositiveIntegerField(verbose_name='Durasi Default (menit)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Status')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')

    class Meta:
        db_table = 'courses'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f'{self.code} - {self.name}'


class Level(SoftDeleteModel):
    """
    Menyimpan data Tingkatan (Level) di dalam sebuah Program/Course.
    
    Relasi Database:
    - Many-to-One dengan `Course`.
    - Many-to-One (self) dengan `Level` (sebagai prerequisite/prasyarat).
    
    Efek Penghapusan (Cascade Behavior):
    - Jika `Course` induk dihapus, Level ini TERHAPUS (CASCADE).
    - Jika Level ini dihapus:
      -> `Enrollment` siswa di level ini TERHAPUS (CASCADE).
      -> Prasyarat di level berikutnya akan menjadi NULL (SET_NULL).
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='levels', verbose_name='Kursus')
    code = models.CharField(max_length=20, verbose_name='Kode Level')
    name = models.CharField(max_length=100, verbose_name='Nama Level')
    order = models.PositiveIntegerField(verbose_name='Urutan')
    
    prerequisite = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_levels', verbose_name='Level Prasyarat')
    
    use_course_duration = models.BooleanField(default=True, verbose_name='Gunakan Durasi Kursus')
    custom_duration = models.PositiveIntegerField(blank=True, null=True, verbose_name='Durasi Khusus (menit)')
    estimated_sessions = models.PositiveIntegerField(verbose_name='Estimasi Pertemuan')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Status')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')

    class Meta:
        db_table = 'levels'
        verbose_name_plural = 'Levels'
        unique_together = ('course', 'code')

    def __str__(self):
        return f'{self.course.code} - {self.code} - {self.name}'

class Package(SoftDeleteModel):
    """
    Menyimpan data Paket Bundling / Diskon (misal: Paket 10x Pertemuan, Paket Semester).
    
    Relasi Database:
    - Opsional terhubung ke `Enrollment`, `InvoiceItem`, `StudentQuota`.
    
    Efek Penghapusan (Cascade Behavior):
    - Jika Package ini dihapus:
      -> `Enrollment` yang tadinya menggunakan paket ini HANYA akan menjadi NULL (SET_NULL). Data siswa/pendaftaran AMAN.
      -> Tagihan (`InvoiceItem`) akan SET_NULL.
    """
    levels = models.ManyToManyField('Level', related_name='packages', blank=True, verbose_name='Level yang Berlaku')
    name = models.CharField(max_length=100, verbose_name='Nama Paket')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Harga Paket')
    meetings_quota = models.PositiveIntegerField(verbose_name='Kuota Pertemuan')
    validity_days = models.PositiveIntegerField(verbose_name='Masa Berlaku (Hari)')
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Aktif'), ('INACTIVE', 'Nonaktif')], default='ACTIVE')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'packages'

    def __str__(self):
        return f"{self.name} ({self.meetings_quota} Pertemuan)"

class AcademicYear(SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True, verbose_name='Kode Tahun Ajaran')
    name = models.CharField(max_length=100, verbose_name='Nama Tahun Ajaran', help_text='Misal: 2026/2027')
    start_year = models.PositiveIntegerField(verbose_name='Tahun Mulai')
    end_year = models.PositiveIntegerField(verbose_name='Tahun Selesai')
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Aktif'), ('INACTIVE', 'Nonaktif')], default='ACTIVE')

    class Meta:
        db_table = 'academic_years'

    def __str__(self):
        return self.name

class AcademicPeriod(SoftDeleteModel):
    """
    Menyimpan data Periode Akademik (Semester/Term) yang berjalan.
    
    Relasi Database:
    - Many-to-One dengan `AcademicYear` (Tahun Ajaran).
    
    Efek Penghapusan (Cascade Behavior):
    - Jika `AcademicYear` dihapus, maka seluruh periode di dalamnya TERHAPUS (CASCADE).
    - Jika AcademicPeriod dihapus:
      -> Mapping ke cabang (`BranchAcademicPeriod`) TERHAPUS (CASCADE).
      -> `Enrollment` siswa yang tadinya di periode ini hanya akan menjadi NULL (SET_NULL).
    """
    PERIOD_TYPES = [
        ('SEMESTER', 'Semester'),
        ('TERM', 'Term'),
        ('INTENSIVE', 'Intensif / Spesial')
    ]
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'), ('OPEN', 'Open'), ('LOCKED', 'Locked'), 
        ('CLOSED', 'Closed'), ('ARCHIVED', 'Archived')
    ]

    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='periods', null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Nama Periode')
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPES, default='SEMESTER')
    sequence = models.PositiveIntegerField(default=1)
    
    # Range
    start_date = models.DateField(verbose_name='Tanggal Mulai Periode', null=True, blank=True)
    end_date = models.DateField(verbose_name='Tanggal Selesai Periode', null=True, blank=True)
    registration_start = models.DateField(blank=True, null=True, verbose_name='Pendaftaran Mulai')
    registration_end = models.DateField(blank=True, null=True, verbose_name='Pendaftaran Selesai')
    learning_start = models.DateField(blank=True, null=True, verbose_name='KBM Mulai')
    learning_end = models.DateField(blank=True, null=True, verbose_name='KBM Selesai')
    
    # Coverage
    is_global = models.BooleanField(default=True, verbose_name='Berlaku Semua Cabang')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'academic_periods'

    def __str__(self):
        return f"{self.academic_year.name if self.academic_year else ''} - {self.name}"

class BranchAcademicPeriod(SoftDeleteModel):
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='academic_periods')
    academic_period = models.ForeignKey(AcademicPeriod, on_delete=models.CASCADE, related_name='branch_assignments')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'branch_academic_periods'
        unique_together = ('branch', 'academic_period')

class StudyClass(SoftDeleteModel):
    """
    Menyimpan entitas fisik Kelas Kelompok (misal: Kelas Matematika 1A).
    
    Relasi Database:
    - Many-to-One dengan `Branch` (Cabang) dan `Course` (Kursus).
    - Many-to-One dengan `Employee` (Guru/Coach).
    
    Efek Penghapusan (Cascade Behavior):
    - Jika Cabang atau Kursus dihapus, Kelas ini IKUT TERHAPUS (CASCADE).
    - Jika Kelas ini dihapus:
      -> `Enrollment` siswa di kelas ini menjadi NULL (SET_NULL). Siswa & pendaftarannya tidak hilang.
    - Jika `Employee` (Coach) dihapus, field `coach` di kelas ini menjadi NULL (SET_NULL). Kelas tetap ada.
    """
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='classes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=100, verbose_name='Nama Kelas')
    capacity = models.PositiveIntegerField(verbose_name='Kapasitas')
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Aktif'), ('INACTIVE', 'Nonaktif')], default='ACTIVE')
    
    # Coach can be nullable if assigned later, we will use string reference 'hr.Employee'
    coach = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_classes')

    class Meta:
        db_table = 'study_classes'

    def __str__(self):
        return f"{self.name} - {self.branch.name}"
