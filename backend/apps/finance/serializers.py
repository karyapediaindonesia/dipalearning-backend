from rest_framework import serializers
from .models import PaymentMethod, FeeCategory

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class FeeCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    class Meta:
        model = FeeCategory
        fields = '__all__'
