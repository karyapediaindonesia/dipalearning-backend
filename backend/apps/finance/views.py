from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PaymentMethod, FeeCategory
from .serializers import PaymentMethodSerializer, FeeCategorySerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()

class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()
