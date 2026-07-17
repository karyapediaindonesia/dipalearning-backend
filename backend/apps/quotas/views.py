from rest_framework import viewsets
from .models import StudentQuota, QuotaTransaction
from .serializers import StudentQuotaSerializer, QuotaTransactionSerializer

class StudentQuotaViewSet(viewsets.ModelViewSet):
    queryset = StudentQuota.objects.all().order_by('-created_at')
    serializer_class = StudentQuotaSerializer
    
class QuotaTransactionViewSet(viewsets.ModelViewSet):
    queryset = QuotaTransaction.objects.all().order_by('-created_at')
    serializer_class = QuotaTransactionSerializer
