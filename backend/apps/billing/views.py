from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Invoice, InvoiceItem, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
from apps.quotas.models import StudentQuota, QuotaTransaction

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        
        if payment.status == 'VERIFIED':
            return Response({'detail': 'Payment is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            
        payment.status = 'VERIFIED'
        payment.verified_by = request.user
        payment.verified_at = timezone.now()
        payment.save()
        
        # Update Invoice Status
        invoice = payment.invoice
        invoice.paid_amount += payment.amount
        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = 'PAID'
        else:
            invoice.status = 'PARTIAL'
        invoice.save()

        # Activate Quota automatically based on InvoiceItems
        for item in invoice.items.all():
            if item.package:
                quota, created = StudentQuota.objects.get_or_create(
                    student=invoice.student,
                    package=item.package,
                    defaults={'total_quota': 0, 'balance': 0, 'used_quota': 0}
                )
                
                added_meetings = item.package.meetings_quota
                quota.total_quota += added_meetings
                quota.balance += added_meetings
                quota.status = 'ACTIVE'
                # Set validity based on package.validity_days if needed
                if item.package.validity_days:
                    quota.valid_until = timezone.now().date() + timezone.timedelta(days=item.package.validity_days)
                quota.save()

                QuotaTransaction.objects.create(
                    quota=quota,
                    transaction_type='ADD',
                    amount=added_meetings,
                    reference=f"PAY-{payment.payment_number}"
                )

        return Response({'detail': 'Payment verified and quota activated.'})
