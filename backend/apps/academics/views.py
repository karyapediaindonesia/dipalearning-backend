from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Level, Package, AcademicYear, AcademicPeriod, StudyClass
from .serializers import (
    CourseSerializer, LevelSerializer, PackageSerializer, 
    AcademicYearSerializer, AcademicPeriodSerializer, StudyClassSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("CREATE REQUEST DATA:", request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print("UPDATE REQUEST DATA:", request.data)
        return super().update(request, *args, **kwargs)

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.select_related('course').all().order_by('course__code', 'order')
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        order_list = request.data.get('order', [])
        for idx, obj_id in enumerate(order_list):
            Level.objects.filter(id=obj_id).update(order=idx + 1)
        return Response({'status': 'success'})

    def perform_create(self, serializer):
        max_order = Level.objects.all().order_by('-order').first()
        next_order = (max_order.order + 1) if max_order else 1
        serializer.save(order=next_order)

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

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        order_list = request.data.get('order', [])
        for idx, obj_id in enumerate(order_list):
            AcademicPeriod.objects.filter(id=obj_id).update(sequence=idx + 1)
        return Response({'status': 'success'})

    def perform_create(self, serializer):
        max_seq = AcademicPeriod.objects.all().order_by('-sequence').first()
        next_seq = (max_seq.sequence + 1) if max_seq else 1
        serializer.save(sequence=next_seq)

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
