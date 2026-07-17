from django.db import models
from apps.core.models import SoftDeleteModel

class AbsenceReason(SoftDeleteModel):
    APPLIES_TO_CHOICES = [
        ('STUDENT', 'Siswa'),
        ('COACH', 'Coach'),
        ('BOTH', 'Keduanya'),
    ]

    CLASSIFICATION_CHOICES = [
        ('EXCUSED', 'Excused (Diterima)'),
        ('UNEXCUSED', 'Unexcused (Ditolak)'),
        ('PENDING_VERIFICATION', 'Menunggu Verifikasi'),
    ]

    MAKEUP_ELIGIBLE_CHOICES = [
        ('ELIGIBLE', 'Berhak Make-up'),
        ('NOT_ELIGIBLE', 'Tidak Berhak Make-up'),
        ('REQUIRES_APPROVAL', 'Memerlukan Persetujuan'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Kode Alasan")
    name = models.CharField(max_length=100, verbose_name="Nama Alasan")
    applies_to = models.CharField(max_length=20, choices=APPLIES_TO_CHOICES, verbose_name="Berlaku Untuk")
    classification = models.CharField(max_length=50, choices=CLASSIFICATION_CHOICES, verbose_name="Klasifikasi")
    is_makeup_eligible = models.CharField(max_length=50, choices=MAKEUP_ELIGIBLE_CHOICES, verbose_name="Kebijakan Make-up")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        db_table = 'absence_reasons'
        verbose_name_plural = 'Absence Reasons'

    def __str__(self):
        return f"{self.code} - {self.name}"
