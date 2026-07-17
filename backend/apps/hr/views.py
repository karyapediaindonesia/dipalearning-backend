from rest_framework import viewsets, permissions
from .models import Employee, JobPosition, EmployeeDocument
from .serializers import (
    EmployeeSerializer, 
    JobPositionSerializer,
    EmployeeDocumentSerializer
)

class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all().order_by('name')
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        job_title = self.request.query_params.get('job_title')
        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)
        return queryset

class EmployeeDocumentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDocument.objects.all()
    serializer_class = EmployeeDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
