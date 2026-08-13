from rest_framework import viewsets, permissions, status as http_status
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Prospect, ProspectStatusHistory, Student, Enrollment, ProspectStatus
from .serializers import (
    ProspectSerializer, ProspectOptionsSerializer, 
    StudentSerializer, EnrollmentSerializer,
    ProspectStatusSerializer
)

class ProspectStatusViewSet(viewsets.ModelViewSet):
    queryset = ProspectStatus.objects.all().order_by('sequence')
    serializer_class = ProspectStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        order_list = request.data.get('order', [])
        for idx, obj_id in enumerate(order_list):
            ProspectStatus.objects.filter(id=obj_id).update(sequence=idx + 1)
        return Response({'status': 'success'})

    def perform_create(self, serializer):
        max_seq = ProspectStatus.objects.all().order_by('-sequence').first()
        next_seq = (max_seq.sequence + 1) if max_seq else 1
        serializer.save(sequence=next_seq)

class ProspectViewSet(viewsets.ModelViewSet):
    queryset = Prospect.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProspectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        prospect = serializer.save()
        # No more auto-invoice here. Invoice is generated via 'pilih_paket' action.

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def pilih_paket(self, request, pk=None):
        prospect = self.get_object()
        
        # Cek apakah sudah ada tagihan unpaid
        if prospect.invoices.filter(status='UNPAID').exists():
            return Response({'detail': 'Prospek ini sudah memiliki tagihan yang belum lunas.'}, status=status.HTTP_400_BAD_REQUEST)
            
        course_id = request.data.get('course')
        level_id = request.data.get('level')
        package_id = request.data.get('package')
        target_start_date = request.data.get('target_start_date')
        
        if not all([course_id, level_id, package_id, target_start_date]):
            return Response({'detail': 'Semua field (Kursus, Level, Paket, Tanggal Mulai) wajib diisi.'}, status=status.HTTP_400_BAD_REQUEST)
            
        from apps.academics.models import Course, Level, Package
        try:
            course = Course.objects.get(id=course_id)
            level = Level.objects.get(id=level_id)
            package = Package.objects.get(id=package_id)
        except (Course.DoesNotExist, Level.DoesNotExist, Package.DoesNotExist):
            return Response({'detail': 'Data referensi akademik tidak valid.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 1. Simpan minat prospek
        from apps.students.models import ProspectInterest
        ProspectInterest.objects.update_or_create(
            prospect=prospect,
            defaults={
                'course': course,
                'level_estimation': str(level.id),
                'package_interest': str(package.id),
                'target_start_date': target_start_date,
                'interest_notes': f"Memilih {package.name} untuk {course.name} Level {level.name}"
            }
        )
        
        # 2. Generate Tagihan Resmi
        from apps.billing.models import Invoice, InvoiceItem
        registration_fee = 250000
        package_price = package.price
        total_amount = registration_fee + package_price
        
        invoice = Invoice.objects.create(
            prospect=prospect,
            total_amount=total_amount,
            status='UNPAID',
            notes=f'Pendaftaran dan Pembelian Paket: {package.name} - {course.name}'
        )
        
        InvoiceItem.objects.create(
            invoice=invoice,
            description='Biaya Pendaftaran / Registrasi',
            amount=registration_fee
        )
        
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f'Paket Belajar: {package.name} ({course.name} Level {level.name})',
            amount=package_price,
            package=package
        )
        
        return Response({'detail': 'Paket berhasil dipilih dan tagihan telah diterbitkan.'})

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'])
    def options(self, request):
        """
        Endpoint to provide choices (master data) for frontend dropdowns.
        """
        serializer = ProspectOptionsSerializer(instance={})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def convert_to_student(self, request, pk=None):
        prospect = self.get_object()
        
        # Check if already a student
        if hasattr(prospect, 'student_profile') and prospect.student_profile:
            return Response({'student_id': prospect.student_profile.id}, status=http_status.HTTP_200_OK)
            
        if prospect.status and prospect.status.code != 'REG_PAID':
            return Response({'detail': 'Prospek belum lunas pendaftaran.'}, status=http_status.HTTP_400_BAD_REQUEST)
            
        with transaction.atomic():
            student = Student.objects.create(
                prospect=prospect,
                full_name=prospect.full_name,
                status='ACTIVE'
            )
            
            lunas_status, _ = ProspectStatus.objects.get_or_create(
                code='ENROLLED',
                defaults={'name': 'Telah Mendaftar', 'sequence': 60, 'is_success': True}
            )
            prospect.status = lunas_status
            prospect.save()
            
        return Response({'student_id': student.id}, status=http_status.HTTP_201_CREATED)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('-created_at')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().order_by('-created_at')
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        enrollment = serializer.save()
        
        # Auto generate invoice for the course
        amount = 500000 # default
        if enrollment.package and enrollment.package.price:
            amount = enrollment.package.price
            
        from apps.billing.models import Invoice, InvoiceItem
        invoice = Invoice.objects.create(
            student=enrollment.student,
            total_amount=amount,
            status='UNPAID',
            notes=f'Tagihan Kursus: {enrollment.course.name} - {enrollment.level.name}'
        )
        InvoiceItem.objects.create(
            invoice=invoice,
            description=f'Biaya Program {enrollment.course.name}',
            amount=amount
        )
        
        # Link invoice back to enrollment if necessary, or just keep it in Student
        enrollment.invoice_id = invoice.invoice_number
        enrollment.save(update_fields=['invoice_id'])
        
        # Create initial history
        EnrollmentHistory.objects.create(
            enrollment=enrollment,
            change_type='NEW_ENROLLMENT',
            after_data=f"Status: {enrollment.status}, Course: {enrollment.course.name}, Class: {enrollment.study_class.name if enrollment.study_class else '-'}",
            reason="Initial Enrollment",
            changed_by=self.request.user if self.request.user.is_authenticated else None
        )

    @transaction.atomic
    def perform_update(self, serializer):
        original = self.get_object()
        original_status = original.status
        original_class = original.study_class

        updated = serializer.save()

        # Log changes if any
        changes = []
        if original_status != updated.status:
            changes.append(f"Status: {original_status} -> {updated.status}")
        if original_class != updated.study_class:
            c1 = original_class.name if original_class else 'None'
            c2 = updated.study_class.name if updated.study_class else 'None'
            changes.append(f"Class: {c1} -> {c2}")
        
        if changes:
            EnrollmentHistory.objects.create(
                enrollment=updated,
                change_type='UPDATE_ENROLLMENT',
                before_data=f"Status: {original_status}, Class: {original_class.name if original_class else '-'}",
                after_data=", ".join(changes),
                reason=self.request.data.get('notes', 'Updated via API'),
                changed_by=self.request.user if self.request.user.is_authenticated else None
            )
