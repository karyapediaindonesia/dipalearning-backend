from django.db import models
from django.conf import settings
from apps.core.models import SoftDeleteModel

class Branch(SoftDeleteModel):
    """
    Menyimpan data Cabang (Branch) dari institusi/perusahaan.
    
    Relasi Database:
    - Many-to-One (self): `parent_branch` menunjuk ke Branch lain sebagai induk.
    - Many-to-One dengan `User` (`person_in_charge`): User yang menjadi penanggung jawab cabang ini.
    - Digunakan oleh sangat banyak model lain (Room, Holiday, Enrollment, Prospect, dll).
    
    Efek Penghapusan (Cascade Behavior):
    - Model ini menggunakan SoftDeleteModel (is_deleted=True saat dihapus).
    - Jika Branch dihapus secara Hard Delete:
      -> `Room` (Ruangan) di cabang ini akan TERHAPUS (CASCADE).
      -> `Holiday` (Libur) di cabang ini akan TERHAPUS (CASCADE).
      -> `Enrollment` (Pendaftaran) di cabang ini akan TERHAPUS (CASCADE).
      -> Relasi M2M ke User (`assigned_branches`) terputus aman.
      -> Data `Prospect` (Calon Siswa) yang menunjuk ke cabang ini akan menjadi NULL (SET_NULL).
    """
    BRANCH_TYPE_CHOICES = [
        ('HEAD_OFFICE', 'Kantor Pusat'),
        ('BRANCH', 'Cabang'),
        ('SUB_BRANCH', 'Cabang Pembantu'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
        ('CLOSED', 'Tutup'),
    ]

    TIMEZONE_CHOICES = [
        ('Asia/Jakarta', 'WIB (Asia/Jakarta)'),
        ('Asia/Makassar', 'WITA (Asia/Makassar)'),
        ('Asia/Jayapura', 'WIT (Asia/Jayapura)'),
    ]

    # --- 1. Identitas Cabang ---
    code = models.CharField(max_length=20, unique=True, verbose_name="Kode Cabang")
    name = models.CharField(max_length=100, verbose_name="Nama Cabang")
    short_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nama Singkat")
    branch_type = models.CharField(max_length=20, choices=BRANCH_TYPE_CHOICES, verbose_name="Jenis Cabang")
    logo = models.ImageField(upload_to='branches/logos/', blank=True, null=True, verbose_name="Logo Cabang")

    # --- 2. Alamat Cabang ---
    address = models.TextField(verbose_name="Alamat Lengkap")
    province = models.CharField(max_length=100, verbose_name="Provinsi")
    city = models.CharField(max_length=100, verbose_name="Kota/Kabupaten")
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kecamatan")
    sub_district = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kelurahan/Desa")
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Kode Pos")
    map_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lokasi Peta")

    # --- 3. Kontak dan Penanggung Jawab ---
    whatsapp_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nomor WhatsApp")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Cabang")
    
    # --- Relasi Database ---
    parent_branch = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_branches', verbose_name="Cabang Induk")
    person_in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_branches', verbose_name="Penanggung Jawab")

    # --- 4. Status dan Administrasi ---
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='Asia/Jakarta', verbose_name="Zona Waktu")
    operational_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Mulai Operasional")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status Cabang")
    status_effective_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Efektif Status")
    deactivation_reason = models.TextField(blank=True, null=True, verbose_name="Alasan Nonaktif/Penutupan")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def pic_position(self):
        """Jabatan Penanggung Jawab (Read-only, Otomatis)"""
        if self.person_in_charge:
            roles = self.person_in_charge.roles.all()
            if roles.exists():
                return ", ".join([role.name for role in roles])
        return "-"

    @property
    def pic_contact(self):
        """Kontak Penanggung Jawab (Read-only, Otomatis)"""
        if self.person_in_charge:
            return self.person_in_charge.email
        return "-"


class Room(SoftDeleteModel):
    """
    Menyimpan data Ruangan fisik di dalam sebuah Cabang.
    
    Relasi Database:
    - Many-to-One dengan `Branch` (Cabang).
    
    Efek Penghapusan (Cascade Behavior):
    - Jika `Branch` (Cabang Induk) dihapus (Hard Delete), maka Room ini TERHAPUS permanen (CASCADE).
    - Menghapus Room tidak berdampak ke cabang.
    """
    ROOM_TYPE_CHOICES = [
        ('CLASSROOM', 'Ruang Kelas'),
        ('PRIVATE', 'Ruang Privat'),
        ('GROUP', 'Ruang Kelompok'),
        ('LABORATORY', 'Laboratorium'),
        ('MEETING', 'Ruang Rapat'),
        ('HALL', 'Aula/Multifungsi'),
        ('ADMINISTRATION', 'Ruang Administrasi'),
        ('OTHER', 'Lainnya'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='rooms', verbose_name='Cabang')
    code = models.CharField(max_length=20, verbose_name='Kode Ruangan')
    name = models.CharField(max_length=100, verbose_name='Nama Ruangan')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, verbose_name='Jenis Ruangan')
    
    capacity_ideal = models.PositiveIntegerField(verbose_name='Kapasitas Ideal')
    capacity_max = models.PositiveIntegerField(verbose_name='Kapasitas Maksimal')
    
    # Facilities can be stored as JSON
    facilities = models.JSONField(blank=True, null=True, default=list, verbose_name='Fasilitas Ruangan')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Status Ruangan')
    
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')

    class Meta:
        db_table = 'rooms'
        verbose_name_plural = 'Rooms'
        unique_together = ('branch', 'code')

    def __str__(self):
        return f'{self.code} - {self.name} ({self.branch.code})'



class Holiday(SoftDeleteModel):
    """
    Menyimpan data Hari Libur atau event khusus yang berdampak pada operasional Cabang.
    
    Relasi Database:
    - Many-to-One dengan `Branch` (Cabang).
    
    Efek Penghapusan (Cascade Behavior):
    - Jika `Branch` dihapus (Hard Delete), maka data liburan ini TERHAPUS (CASCADE).
    """
    HOLIDAY_TYPE_CHOICES = [
        ('NATIONAL', 'Nasional'),
        ('JOINT_LEAVE', 'Cuti Bersama'),
        ('ACADEMIC_HOLIDAY', 'Libur Akademik'),
        ('BRANCH_HOLIDAY', 'Libur Cabang'),
        ('INTERNAL_EVENT', 'Kegiatan Internal'),
        ('MAINTENANCE', 'Maintenance'),
        ('SPECIAL_CONDITION', 'Keadaan Khusus'),
    ]

    IMPACT_CHOICES = [
        ('FULL_CLOSE', 'Cabang Tutup Total'),
        ('NO_CLASS_ADMIN_OPEN', 'Tidak Ada Kelas, Admin Tetap Buka'),
        ('LIMITED_OPERATIONS', 'Operasional Terbatas'),
        ('SPECIFIC_ACTIVITY_CLOSED', 'Hanya Kegiatan Tertentu Ditutup'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='holidays', verbose_name='Cabang')
    name = models.CharField(max_length=100, verbose_name='Nama Libur/Kegiatan')
    holiday_type = models.CharField(max_length=50, choices=HOLIDAY_TYPE_CHOICES, verbose_name='Jenis Hari Libur')
    date_start = models.DateField(verbose_name='Tanggal Mulai')
    date_end = models.DateField(verbose_name='Tanggal Selesai')
    operational_impact = models.CharField(max_length=50, choices=IMPACT_CHOICES, verbose_name='Dampak Operasional')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Status')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')

    class Meta:
        db_table = 'holidays'
        verbose_name_plural = 'Holidays'
        unique_together = ('branch', 'name', 'date_start')

    def __str__(self):
        return f'{self.name} ({self.date_start} - {self.date_end})'
