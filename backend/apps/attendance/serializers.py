from rest_framework import serializers
from .models import AbsenceReason

class AbsenceReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceReason
        fields = '__all__'
