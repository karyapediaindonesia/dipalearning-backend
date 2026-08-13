from rest_framework import serializers
from .models import (
    Prospect, ProspectParent, ProspectGuardian, ProspectAddress, ProspectSource, 
    ProspectInterest, ProspectStatusHistory, Student, Enrollment, EnrollmentHistory,
    GENDER_CHOICES, EDU_STATUS_CHOICES, EDU_LEVEL_CHOICES, RELATION_CHOICES,
    COMM_PREF_CHOICES, SOURCE_CHOICES, ProspectStatus
)
from apps.branches.serializers import BranchSerializer
from apps.academics.serializers import CourseSerializer
from django.db import transaction

class ProspectParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectParent
        exclude = ('prospect', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class ProspectAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectAddress
        exclude = ('prospect', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class ProspectStatusSerializer(serializers.ModelSerializer):
    sequence = serializers.IntegerField(required=False)
    class Meta:
        model = ProspectStatus
        fields = '__all__'

class ProspectSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectSource
        exclude = ('prospect', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class ProspectInterestSerializer(serializers.ModelSerializer):
    # course_details = CourseSerializer(source='course', read_only=True)
    class Meta:
        model = ProspectInterest
        exclude = ('prospect', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class ProspectGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectGuardian
        exclude = ('prospect', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class ProspectStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectStatusHistory
        fields = '__all__'

class ProspectSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        slug_field='code',
        queryset=ProspectStatus.objects.all(),
        required=False,
        allow_null=True
    )
    parent = ProspectParentSerializer(required=False, allow_null=True)
    guardian = ProspectGuardianSerializer(required=False, allow_null=True)
    address = ProspectAddressSerializer(required=False, allow_null=True)
    source = ProspectSourceSerializer(required=False, allow_null=True)
    interests = ProspectInterestSerializer(many=True, required=False, allow_null=True)
    
    # Read-only nested fields for display
    invoice_details = serializers.SerializerMethodField()
    # target_branch_details = BranchSerializer(source='target_branch', read_only=True)

    def get_invoice_details(self, obj):
        # Ambil invoice pertama yang belum lunas
        invoice = obj.invoices.filter(status='UNPAID').first()
        if invoice:
            return {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'total_amount': invoice.total_amount,
                'status': invoice.status
            }
        return None

    class Meta:
        model = Prospect
        fields = '__all__'
        read_only_fields = ('prospect_number', 'is_active', 'deleted_at', 'created_by', 'updated_by', 'version')

    @transaction.atomic
    def create(self, validated_data):
        parent_data = validated_data.pop('parent', None)
        guardian_data = validated_data.pop('guardian', None)
        address_data = validated_data.pop('address', None)
        source_data = validated_data.pop('source', None)
        interests_data = validated_data.pop('interests', [])

        prospect = Prospect.objects.create(**validated_data)

        if parent_data:
            ProspectParent.objects.create(prospect=prospect, **parent_data)
        if guardian_data:
            ProspectGuardian.objects.create(prospect=prospect, **guardian_data)
        if address_data:
            ProspectAddress.objects.create(prospect=prospect, **address_data)
        if source_data:
            ProspectSource.objects.create(prospect=prospect, **source_data)
        if interests_data:
            for item in interests_data:
                ProspectInterest.objects.create(prospect=prospect, **item)
        
        return prospect

    @transaction.atomic
    def update(self, instance, validated_data):
        parent_data = validated_data.pop('parent', None)
        address_data = validated_data.pop('address', None)
        source_data = validated_data.pop('source', None)
        interests_data = validated_data.pop('interests', None)

        # Handle status history if status changed
        new_status = validated_data.get('status')
        if new_status and new_status != instance.status:
            request = self.context.get('request')
            user = request.user if request and request.user.is_authenticated else None
            ProspectStatusHistory.objects.create(
                prospect=instance,
                old_status=instance.status,
                new_status=new_status,
                changed_by=user
            )

        # Update Prospect
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Parent
        if parent_data is not None:
            if hasattr(instance, 'parent'):
                for attr, value in parent_data.items():
                    setattr(instance.parent, attr, value)
                instance.parent.save()
            else:
                ProspectParent.objects.create(prospect=instance, **parent_data)

        # Update Guardian
        guardian_data = validated_data.pop('guardian', None)
        if guardian_data is not None:
            if hasattr(instance, 'guardian'):
                for attr, value in guardian_data.items():
                    setattr(instance.guardian, attr, value)
                instance.guardian.save()
            else:
                ProspectGuardian.objects.create(prospect=instance, **guardian_data)

        # Update Address
        if address_data is not None:
            if hasattr(instance, 'address'):
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                ProspectAddress.objects.create(prospect=instance, **address_data)

        # Update Source
        if source_data is not None:
            if hasattr(instance, 'source'):
                for attr, value in source_data.items():
                    setattr(instance.source, attr, value)
                instance.source.save()
            else:
                ProspectSource.objects.create(prospect=instance, **source_data)

        # Update Interests
        if interests_data is not None:
            instance.interests.all().delete()
            for item in interests_data:
                ProspectInterest.objects.create(prospect=instance, **item)

        return instance

class ProspectOptionsSerializer(serializers.Serializer):
    gender = serializers.SerializerMethodField()
    edu_status = serializers.SerializerMethodField()
    edu_level = serializers.SerializerMethodField()
    relation = serializers.SerializerMethodField()
    comm_preference = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    prospect_status = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return [{'value': k, 'label': v} for k, v in GENDER_CHOICES]

    def get_edu_status(self, obj):
        return [{'value': k, 'label': v} for k, v in EDU_STATUS_CHOICES]

    def get_edu_level(self, obj):
        return [{'value': k, 'label': v} for k, v in EDU_LEVEL_CHOICES]

    def get_relation(self, obj):
        return [{'value': k, 'label': v} for k, v in RELATION_CHOICES]

    def get_comm_preference(self, obj):
        return [{'value': k, 'label': v} for k, v in COMM_PREF_CHOICES]

    def get_source(self, obj):
        return [{'value': k, 'label': v} for k, v in SOURCE_CHOICES]
        
    def get_prospect_status(self, obj):
        statuses = ProspectStatus.objects.filter(status=True).order_by('sequence')
        return [{'value': s.id, 'label': s.name, 'code': s.code, 'color': s.color} for s in statuses]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('student_number',)

class EnrollmentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentHistory
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    histories = EnrollmentHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('enrollment_no',)
