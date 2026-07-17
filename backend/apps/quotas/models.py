from django.db import models
from apps.core.models import SoftDeleteModel
from apps.students.models import Student
from apps.academics.models import Package

class StudentQuota(SoftDeleteModel):
    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('EXPIRED', 'Kedaluwarsa'),
        ('DEPLETED', 'Habis'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quotas')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    
    total_quota = models.PositiveIntegerField(default=0, verbose_name='Total Kuota Dibeli')
    used_quota = models.PositiveIntegerField(default=0, verbose_name='Kuota Terpakai')
    balance = models.PositiveIntegerField(default=0, verbose_name='Sisa Kuota')
    
    valid_from = models.DateField(auto_now_add=True)
    valid_until = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        db_table = 'student_quotas'

    def __str__(self):
        return f"Kuota {self.student.full_name} - Sisa {self.balance}"

    def check_status(self):
        if self.balance <= 0:
            self.status = 'DEPLETED'
        # Add logic for expired check if needed

class QuotaTransaction(SoftDeleteModel):
    TYPE_CHOICES = [
        ('ADD', 'Penambahan'),
        ('DEDUCT', 'Pengurangan'),
        ('ADJUST', 'Penyesuaian Manual'),
    ]

    quota = models.ForeignKey(StudentQuota, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=100, blank=True, null=True, help_text='Nomor Invoice / Nomor Absen')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'quota_transactions'
