import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import BaseModel, SoftDeleteModel
from apps.branches.models import Branch


class Permission(BaseModel):
    """
    Menyimpan data hak akses (Permission) spesifik di luar bawaan Django.
    
    Relasi Database:
    - Many-to-Many dengan `Role`: Sebuah Permission bisa dimiliki banyak Role.
    
    Efek Penghapusan (Cascade Behavior):
    - Jika Permission dihapus, relasinya dengan Role akan terputus (baris di tabel perantara dihapus), 
      namun Role itu sendiri TIDAK akan ikut terhapus.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Permission")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")

    def __str__(self):
        return self.name


class Role(SoftDeleteModel):
    """
    Menyimpan data Peran (Role) pengguna, seperti 'Admin', 'Kepala Cabang', dll.
    
    Relasi Database:
    - Many-to-Many dengan `Permission` (Tabel `permissions`).
    - Many-to-Many dengan `User` (Tabel `User.roles`).
    
    Efek Penghapusan (Cascade Behavior):
    - Model ini menggunakan SoftDeleteModel (is_deleted=True saat dihapus).
    - Jika Role ini benar-benar dihapus permanen (Hard Delete):
      -> Hubungannya dengan User (User.roles) akan terputus, namun User TIDAK ikut terhapus.
      -> Hubungannya dengan Permission terputus, Permission TIDAK ikut terhapus.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Role")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Role")
    
    # --- Relasi ---
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="Hak Akses")

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Tabel utama Pengguna (Karyawan/Siswa yang bisa login). Meng-extend `AbstractUser` bawaan Django.
    
    Atribut Bawaan Django (AbstractUser):
    - username, first_name, last_name, email, is_staff, is_active, date_joined, password
    
    Relasi Database:
    - Many-to-Many dengan `Role`: Satu user bisa punya banyak peran.
    - Many-to-Many dengan `Branch` (assigned_branches): Satu user bisa ditugaskan di banyak cabang.
    
    Efek Penghapusan (Cascade Behavior):
    - Menghapus User berpotensi sangat destruktif karena banyak tabel bergantung padanya!
    - Jika User dihapus:
      -> Relasi M2M ke Role & Branch terputus aman.
      -> (Di tabel lain): Jika User adalah `person_in_charge` di Cabang, field tersebut menjadi NULL (SET_NULL).
      -> (Di tabel lain): Jika User punya Employee/Coach/Prospect, profil mereka mungkin ikut TERHAPUS (CASCADE) atau menjadi NULL, tergantung aturan tabel tsb.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email Akun")
    
    # --- Relasi ---
    roles = models.ManyToManyField(Role, blank=True, verbose_name="Peran (Roles)")
    assigned_branches = models.ManyToManyField(Branch, blank=True, verbose_name="Cabang Penugasan")
    
    # --- Atribut Tambahan ---
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Foto Profil")
    failed_login_attempts = models.IntegerField(default=0, verbose_name="Gagal Login (Kali)")
    is_locked = models.BooleanField(default=False, verbose_name="Akun Terkunci")
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="Terkunci Sampai")
    
    def __str__(self):
        return self.username
