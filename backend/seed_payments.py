import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.finance.models import PaymentMethod

print("Seeding Payment Methods...")

payment_methods = [
    {
        'code': 'CASH',
        'name': 'Tunai (Cash)',
        'processing_mode': 'MANUAL',
        'requires_reference': False,
        'notes': 'Pembayaran tunai di kasir/resepsionis.'
    },
    {
        'code': 'TRF-BCA',
        'name': 'Transfer Bank BCA',
        'processing_mode': 'MANUAL',
        'requires_reference': True,
        'notes': 'Transfer ke rekening BCA Dipa Learning Center. Wajib lampirkan bukti/nomor referensi.'
    },
    {
        'code': 'TRF-MANDIRI',
        'name': 'Transfer Bank Mandiri',
        'processing_mode': 'MANUAL',
        'requires_reference': True,
        'notes': 'Transfer ke rekening Mandiri.'
    },
    {
        'code': 'QRIS',
        'name': 'QRIS (Gopay/OVO/ShopeePay)',
        'processing_mode': 'SEMI_AUTO',
        'requires_reference': True,
        'notes': 'Pembayaran melalui scan barcode QRIS.'
    },
    {
        'code': 'VA-BCA',
        'name': 'BCA Virtual Account (Otomatis)',
        'processing_mode': 'AUTO',
        'requires_reference': False,
        'notes': 'Pembayaran VA otomatis terkonfirmasi oleh sistem.'
    }
]

for pm_data in payment_methods:
    obj, created = PaymentMethod.objects.get_or_create(
        code=pm_data['code'],
        defaults=pm_data
    )
    if created:
        print(f"Created: {obj.name}")
    else:
        print(f"Already exists: {obj.name}")

print(f"Total Payment Methods: {PaymentMethod.objects.count()}")
