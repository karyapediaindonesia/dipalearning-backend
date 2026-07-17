from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AbsenceReason
from .serializers import AbsenceReasonSerializer

class AbsenceReasonViewSet(viewsets.ModelViewSet):
    queryset = AbsenceReason.objects.all()
    serializer_class = AbsenceReasonSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.delete()
