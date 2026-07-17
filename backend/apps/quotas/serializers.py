from rest_framework import serializers
from .models import StudentQuota, QuotaTransaction

class QuotaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotaTransaction
        fields = '__all__'

class StudentQuotaSerializer(serializers.ModelSerializer):
    transactions = QuotaTransactionSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    package_name = serializers.CharField(source='package.name', read_only=True)

    class Meta:
        model = StudentQuota
        fields = '__all__'
