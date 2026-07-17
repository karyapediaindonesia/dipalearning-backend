from rest_framework import viewsets, permissions
from .models import Course, Level, Package, AcademicYear, AcademicPeriod, StudyClass
from .serializers import (
    CourseSerializer, LevelSerializer, PackageSerializer, 
    AcademicYearSerializer, AcademicPeriodSerializer, StudyClassSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.select_related('course').all().order_by('course__code', 'order')
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated]

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by('name')
    serializer_class = PackageSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all().order_by('-start_year')
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcademicPeriodViewSet(viewsets.ModelViewSet):
    queryset = AcademicPeriod.objects.all().order_by('-start_date')
    serializer_class = AcademicPeriodSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudyClassViewSet(viewsets.ModelViewSet):
    queryset = StudyClass.objects.all().order_by('name')
    serializer_class = StudyClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        branch_id = self.request.query_params.get('branch_id')
        course_id = self.request.query_params.get('course_id')
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset
