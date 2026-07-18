from django.db import models
from apps.core.models import SoftDeleteModel

class PaymentMethod(SoftDeleteModel):
    PROCESSING_CHOICES = [
        ('MANUAL', 'Manual'),
        ('SEMI_AUTO', 'Semi-Otomatis'),
        ('AUTO', 'Otomatis'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Kode Metode")
    name = models.CharField(max_length=100, verbose_name="Nama Metode (Contoh: Transfer BCA)")
    processing_mode = models.CharField(max_length=20, choices=PROCESSING_CHOICES, default='MANUAL', verbose_name="Mode Pemrosesan")
    requires_reference = models.BooleanField(default=True, verbose_name="Wajib Nomor Referensi")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan Tambahan")

    class Meta:
        db_table = 'payment_methods'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def delete(self, using=None, keep_parents=False):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Check if this method has been used in any Payment transaction
        from apps.billing.models import Payment
        if Payment.objects.filter(payment_method=self).exists():
            raise ValidationError("Metode pembayaran tidak dapat dihapus karena pernah digunakan dalam transaksi.")
            
        # HARD DELETE
        return super().delete(using=using, keep_parents=keep_parents)


class FeeCategory(SoftDeleteModel):
    CLASSIFICATION_CHOICES = [
        ('OPEX', 'Operasional/OPEX'),
        ('CAPEX', 'Investasi/CAPEX'),
        ('COGS', 'Harga Pokok/COGS'),
        ('ADMIN', 'Administrasi'),
        ('ACADEMIC', 'Akademik'),
        ('MARKETING', 'Pemasaran'),
        ('HR', 'HR / SDM'),
        ('INVENTORY', 'Inventaris'),
        ('OTHER', 'Lainnya'),
    ]

    NATURE_CHOICES = [
        ('FIXED', 'Tetap'),
        ('VARIABLE', 'Variabel'),
        ('PERIODIC', 'Berkala'),
        ('ONE_TIME', 'Satu Kali'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Aktif'),
        ('INACTIVE', 'Nonaktif'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Kode Kategori")
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories', verbose_name="Kategori Induk")
    
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, verbose_name="Klasifikasi Biaya")
    cost_nature = models.CharField(max_length=20, choices=NATURE_CHOICES, verbose_name="Sifat Biaya")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        db_table = 'fee_categories'
        verbose_name_plural = 'Fee Categories'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def delete(self, using=None, keep_parents=False):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Check if there are active subcategories
        if self.subcategories.filter(is_active=True).exists():
            raise ValidationError("Kategori biaya tidak dapat dihapus karena masih memiliki subkategori aktif.")
            
        # HARD DELETE
        return super().delete(using=using, keep_parents=keep_parents)
