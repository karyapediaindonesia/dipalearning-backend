from django.db import models
from apps.core.models import SoftDeleteModel
from apps.students.models import Student

class Invoice(SoftDeleteModel):
    STATUS_CHOICES = [
        ('UNPAID', 'Belum Lunas'),
        ('PARTIAL', 'Cicilan'),
        ('PAID', 'Lunas'),
        ('VOID', 'Dibatalkan'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name='Nomor Tagihan')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    prospect = models.ForeignKey('students.Prospect', on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    date_issued = models.DateField(auto_now_add=True, verbose_name='Tanggal Terbit')
    due_date = models.DateField(verbose_name='Jatuh Tempo', null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'invoices'

    def __str__(self):
        owner = self.student.full_name if self.student else (self.prospect.full_name if self.prospect else "Unknown")
        return f"{self.invoice_number} - {owner}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            count = Invoice.objects.count() + 1
            self.invoice_number = f"INV-2026-{count:05d}"
        super().save(*args, **kwargs)

class InvoiceItem(SoftDeleteModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, verbose_name='Deskripsi')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Ref to Package id to easily activate quota later
    package = models.ForeignKey('academics.Package', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'invoice_items'

class Payment(SoftDeleteModel):
    STATUS_CHOICES = [
        ('PENDING', 'Menunggu Verifikasi'),
        ('VERIFIED', 'Terverifikasi'),
        ('REJECTED', 'Ditolak'),
    ]
    
    payment_number = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.ForeignKey('finance.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'payments'

    def save(self, *args, **kwargs):
        if not self.payment_number:
            count = Payment.objects.count() + 1
            self.payment_number = f"PAY-2026-{count:05d}"
        super().save(*args, **kwargs)
