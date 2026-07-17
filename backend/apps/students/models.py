from django.db import models
import uuid
from apps.core.models import SoftDeleteModel
from apps.branches.models import Branch
from apps.accounts.models import User
from apps.academics.models import Course # assuming course exists

# Lookup Data options
GENDER_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]
EDU_STATUS_CHOICES = [('STUDENT', 'Pelajar'), ('WORKING', 'Bekerja'), ('NOT_WORKING', 'Tidak Bekerja')]
EDU_LEVEL_CHOICES = [('PAUD_TK', 'PAUD/TK'), ('SD', 'SD'), ('SMP', 'SMP'), ('SMA', 'SMA'), ('MAHASISWA', 'Mahasiswa'), ('UMUM', 'Umum')]
RELATION_CHOICES = [('AYAH', 'Ayah'), ('IBU', 'Ibu'), ('WALI', 'Wali'), ('SAUDARA', 'Saudara'), ('LAINNYA', 'Lainnya')]
COMM_PREF_CHOICES = [('WHATSAPP', 'WhatsApp'), ('EMAIL', 'Email'), ('TELEPON', 'Telepon'), ('SMS', 'SMS')]
SOURCE_CHOICES = [('WEBSITE', 'Website'), ('INSTAGRAM', 'Instagram'), ('FACEBOOK', 'Facebook'), ('TIKTOK', 'TikTok'), ('GOOGLE', 'Google Search'), ('WHATSAPP', 'WhatsApp'), ('REFERRAL', 'Referral Orang Tua'), ('SCHOOL', 'Sekolah'), ('EVENT', 'Event'), ('BROCHURE', 'Brosur'), ('TELEMARKETING', 'Telemarketing'), ('WALKIN', 'Walk-in')]

class ProspectStatus(SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    sequence = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    
    is_initial = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    allow_conversion = models.BooleanField(default=False)
    requires_followup = models.BooleanField(default=False)
    
    probability = models.PositiveIntegerField(default=0, help_text="Persentase keberhasilan 0-100")
    color = models.CharField(max_length=20, default='primary', help_text="Warna label / class badge")
    status = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        db_table = 'prospect_statuses'
        ordering = ['sequence']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Prospect(SoftDeleteModel):
    """
    Menyimpan data Calon Siswa (Prospect) yang tertarik untuk mendaftar.
    Ini adalah entitas utama sebelum mereka resmi menjadi Siswa (Student).
    
    Relasi Database (One-to-One):
    - `parent`, `address`, `source`, `guardian`: Data profil pelengkap (semua One-to-One).
      -> Efek: Jika Prospect dihapus, 4 data pelengkap ini otomatis IKUT TERHAPUS (CASCADE).
      -> Jika salah satu data pelengkap dihapus, Prospect juga ikut TERHAPUS (CASCADE dari sisi reverse).
    
    Relasi Database (Many-to-One):
    - `status` (ProspectStatus): Status calon siswa saat ini. SET_NULL jika status master dihapus.
    - `pic_followup` (User): Pegawai yang melayani. SET_NULL jika user dihapus.
    - `target_branch` & `alt_branch` (Branch): Cabang tujuan. SET_NULL jika cabang dihapus.
    
    Relasi ke Student:
    - `student_profile` (Tabel Student memiliki O2O ke Prospect).
      -> Jika Prospect dihapus, Student TIDAK terhapus, kolom prospect_id di Student jadi NULL (SET_NULL).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prospect_number = models.CharField(max_length=50, unique=True, blank=True)
    full_name = models.CharField(max_length=100, verbose_name='Nama Lengkap Calon Siswa')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nama Panggilan')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Jenis Kelamin')
    place_of_birth = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tempat Lahir')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir')
    nik_nisn = models.CharField(max_length=50, blank=True, null=True, verbose_name='NIK/NISN')
    photo = models.ImageField(upload_to='prospects/photos/', blank=True, null=True, verbose_name='Foto Calon Siswa')

    # Informasi Pendidikan
    edu_status = models.CharField(max_length=20, choices=EDU_STATUS_CHOICES, verbose_name='Status Pendidikan')
    school_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Sekolah')
    edu_level = models.CharField(max_length=20, choices=EDU_LEVEL_CHOICES, verbose_name='Jenjang Sekolah')
    current_class = models.CharField(max_length=50, blank=True, null=True, verbose_name='Kelas Saat Ini')
    school_entry_year = models.IntegerField(blank=True, null=True, verbose_name='Tahun Masuk Sekolah')

    # Informasi Kebutuhan Belajar
    learning_goals = models.JSONField(default=list, verbose_name='Tujuan Mengikuti Kursus') # multi-select
    current_ability = models.TextField(blank=True, null=True, verbose_name='Kemampuan Saat Ini')
    academic_notes = models.TextField(blank=True, null=True, verbose_name='Catatan Akademik')

    # Status & Follow Up
    status = models.ForeignKey(ProspectStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospects', verbose_name='Status Prospect')
    pic_followup = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospect_followups', verbose_name='PIC Follow-up')
    last_followup_date = models.DateField(auto_now=True, verbose_name='Tanggal Follow-up Terakhir')
    next_followup_date = models.DateField(blank=True, null=True, verbose_name='Follow-up Berikutnya')
    followup_notes = models.TextField(blank=True, null=True, verbose_name='Catatan Follow-up')
    lost_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alasan Tidak Lanjut')

    # Branch Target
    target_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='prospect_target_branches', verbose_name='Cabang Tujuan')
    distance_from_home = models.FloatField(blank=True, null=True, verbose_name='Jarak dari Rumah (km)')
    branch_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alasan Memilih Cabang')
    alt_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospect_alt_branches', verbose_name='Cabang Alternatif')

    class Meta:
        db_table = 'prospects'
        verbose_name_plural = 'Prospects'

    def __str__(self):
        return f"{self.prospect_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.prospect_number:
            count = Prospect.objects.count() + 1
            self.prospect_number = f"PRS-2026-{count:05d}"
        super().save(*args, **kwargs)

class ProspectParent(SoftDeleteModel):
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='parent')
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES, verbose_name='Hubungan dengan Siswa')
    full_name = models.CharField(max_length=100, verbose_name='Nama Orang Tua/Wali')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Jenis Kelamin')
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name='Pekerjaan')
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Perusahaan')

    whatsapp = models.CharField(max_length=50, verbose_name='Nomor WhatsApp')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nomor Telepon')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    comm_preference = models.CharField(max_length=20, choices=COMM_PREF_CHOICES, blank=True, null=True, verbose_name='Preferensi Komunikasi')

    payer_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nama Penanggung Jawab Pembayaran')
    payer_relation = models.CharField(max_length=20, choices=RELATION_CHOICES, blank=True, null=True, verbose_name='Hubungan Payer')
    payment_notes = models.TextField(blank=True, null=True, verbose_name='Catatan Pembayaran')

    class Meta:
        db_table = 'prospect_parents'

class ProspectAddress(SoftDeleteModel):
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='address')
    full_address = models.TextField(blank=True, null=True, verbose_name='Alamat Lengkap')
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name='Provinsi')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kota')
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name='Kecamatan')
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Kode Pos')

    class Meta:
        db_table = 'prospect_addresses'

class ProspectSource(SoftDeleteModel):
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='source')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='Sumber Informasi')
    source_detail = models.CharField(max_length=255, blank=True, null=True, verbose_name='Detail Sumber')
    campaign = models.CharField(max_length=255, blank=True, null=True, verbose_name='Campaign')
    referred_by = models.CharField(max_length=255, blank=True, null=True, verbose_name='Referensi Oleh')

    class Meta:
        db_table = 'prospect_sources'

class ProspectInterest(SoftDeleteModel):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='interests')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name='Kursus')
    level_estimation = models.CharField(max_length=50, blank=True, null=True, verbose_name='Level Perkiraan')
    package_interest = models.CharField(max_length=50, blank=True, null=True, verbose_name='Paket Minat')
    target_start_date = models.DateField(blank=True, null=True, verbose_name='Target Mulai')
    interest_notes = models.TextField(blank=True, null=True, verbose_name='Catatan Minat')

    class Meta:
        db_table = 'prospect_interests'

class ProspectStatusHistory(SoftDeleteModel):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='status_histories')
    old_status = models.ForeignKey(ProspectStatus, on_delete=models.SET_NULL, null=True, related_name='old_histories')
    new_status = models.ForeignKey(ProspectStatus, on_delete=models.SET_NULL, null=True, related_name='new_histories')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'prospect_status_history'

class ProspectGuardian(SoftDeleteModel):
    prospect = models.OneToOneField(Prospect, on_delete=models.CASCADE, related_name='guardian')
    guardian_name = models.CharField(max_length=100, verbose_name='Nama Wali')
    relationship = models.CharField(max_length=50, verbose_name='Hubungan dengan Siswa')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Jenis Kelamin')
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name='Pekerjaan')
    phone = models.CharField(max_length=50, verbose_name='Nomor HP/WhatsApp')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    address = models.TextField(blank=True, null=True, verbose_name='Alamat Wali')
    is_primary = models.BooleanField(default=False, verbose_name='Wali Utama')
    status = models.CharField(max_length=20, default='Aktif', verbose_name='Status Wali')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan/Riwayat Perubahan')

    class Meta:
        db_table = 'prospect_guardians'
class Student(SoftDeleteModel):
    """
    Menyimpan data Siswa (Student) yang sudah resmi terdaftar.
    Biasanya dikonversi dari Prospect.
    
    Relasi Database:
    - One-to-One dengan `Prospect`.
      -> Jika Student dihapus, Prospect tetap ADA (tidak cascade balik).
      -> Jika Prospect dihapus, Student tetap ADA (kolom prospect menjadi NULL).
      
    Efek Penghapusan (Cascade Behavior) terhadap relasi lain:
    - Jika Student dihapus:
      -> Seluruh `Enrollment` (Pendaftaran Kelas/Paket) siswa ini akan TERHAPUS (CASCADE).
      -> Seluruh `Invoice` (Tagihan Keuangan) siswa ini akan TERHAPUS (CASCADE).
      -> Data kuota/jadwal privat siswa ini akan TERHAPUS.
    (Hati-hati menghapus Student karena akan merusak data historis pendaftaran dan keuangan!)
    """
    # Core Student Profile (convert from Prospect)
    prospect = models.OneToOneField(Prospect, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    student_number = models.CharField(max_length=50, unique=True, verbose_name='Nomor Siswa')
    full_name = models.CharField(max_length=100, verbose_name='Nama Siswa')
    join_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Aktif'), ('INACTIVE', 'Nonaktif')], default='ACTIVE')

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.student_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.student_number:
            count = Student.objects.count() + 1
            self.student_number = f"STD-2026-{count:05d}"
        super().save(*args, **kwargs)

class Enrollment(SoftDeleteModel):
    """
    Menyimpan data Pendaftaran (Enrollment) siswa ke dalam suatu Kelas atau Paket/Kursus.
    
    Relasi Database:
    - Many-to-One dengan `Student`: Siswa yang mendaftar (Wajib).
    - Many-to-One dengan `Course`, `Level`: Program/Kursus yang diambil (Wajib).
    - Many-to-One dengan `Package`: Paket diskon/bundling (Opsional).
    - Many-to-One dengan `Branch`: Cabang tempat siswa belajar (Wajib).
    - Many-to-One dengan `StudyClass`: Kelas spesifik (jika bentuknya kelas kelompok).
    - Many-to-One dengan `Employee` (Coach): Pengajar khusus (jika privat).
    - Many-to-One dengan `AcademicPeriod`: Periode/Semester berjalan.
    
    Efek Penghapusan (Cascade Behavior):
    - Jika Enrollment dihapus: Data Siswa (Student) TETAP AMAN.
    - Jika `Student` dihapus: Enrollment ini akan IKUT TERHAPUS (CASCADE).
    - Jika `Course`, `Level`, atau `Branch` dihapus (Hard Delete): Enrollment ini IKUT TERHAPUS (CASCADE).
    - Jika `StudyClass`, `Employee` (Coach), `Package`, atau `AcademicPeriod` dihapus: Kolom di Enrollment ini hanya menjadi NULL (SET_NULL), pendaftaran tetap ada.
    """
    ENROLLMENT_STATUS = [
        ('DRAFT', 'Draft'), ('PENDING', 'Pending Payment'), ('ACTIVE', 'Active'), 
        ('SUSPENDED', 'Suspended'), ('COMPLETED', 'Completed'), 
        ('TRANSFERRED', 'Transferred'), ('CANCELLED', 'Cancelled'), ('EXPIRED', 'Expired')
    ]
    
    enrollment_no = models.CharField(max_length=50, unique=True, verbose_name='Nomor Enrollment')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    level = models.ForeignKey('academics.Level', on_delete=models.CASCADE)
    package = models.ForeignKey('academics.Package', on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE)
    study_class = models.ForeignKey('academics.StudyClass', on_delete=models.SET_NULL, null=True, blank=True)
    coach = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    academic_period = models.ForeignKey('academics.AcademicPeriod', on_delete=models.SET_NULL, null=True, blank=True)
    
    enrollment_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='DRAFT')
    
    invoice_id = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'enrollments'

    def __str__(self):
        return self.enrollment_no

    def save(self, *args, **kwargs):
        if not self.enrollment_no:
            count = Enrollment.objects.count() + 1
            self.enrollment_no = f"ENR-2026-{count:05d}"
        super().save(*args, **kwargs)

class EnrollmentHistory(SoftDeleteModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='histories')
    change_date = models.DateTimeField(auto_now_add=True)
    change_type = models.CharField(max_length=100, verbose_name='Jenis Perubahan')
    before_data = models.TextField(blank=True, null=True)
    after_data = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'enrollment_histories'
