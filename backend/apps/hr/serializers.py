from rest_framework import serializers
from .models import Employee, EmployeeBranchAssignment, CoachProfile, EmployeeDocument, EmployeeHistory, JobPosition

class JobPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosition
        fields = '__all__'
from apps.branches.serializers import BranchSerializer
from django.db import transaction

class EmployeeBranchAssignmentSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    class Meta:
        model = EmployeeBranchAssignment
        exclude = ('employee', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class CoachProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachProfile
        exclude = ('employee', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        exclude = ('employee', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class EmployeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHistory
        exclude = ('employee', 'is_active', 'deleted_at', 'created_by', 'updated_by')

class EmployeeSerializer(serializers.ModelSerializer):
    branch_assignments = EmployeeBranchAssignmentSerializer(many=True, required=False)
    coach_profile = CoachProfileSerializer(required=False, allow_null=True)
    documents = EmployeeDocumentSerializer(many=True, read_only=True)
    histories = EmployeeHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('employee_number',)

    @transaction.atomic
    def create(self, validated_data):
        branch_assignments_data = validated_data.pop('branch_assignments', [])
        coach_profile_data = validated_data.pop('coach_profile', None)

        employee = Employee.objects.create(**validated_data)

        # Create branch assignments
        for item in branch_assignments_data:
            EmployeeBranchAssignment.objects.create(employee=employee, **item)

        # Create coach profile if applicable
        if coach_profile_data:
            CoachProfile.objects.create(employee=employee, **coach_profile_data)

        # History log
        request = self.context.get('request')
        user = request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None
        EmployeeHistory.objects.create(
            employee=employee,
            change_type='NEW_EMPLOYEE',
            new_value=f"Job Position: {employee.job_position.name if employee.job_position else ''}",
            changed_by=user
        )

        return employee

    @transaction.atomic
    def update(self, instance, validated_data):
        branch_assignments_data = validated_data.pop('branch_assignments', None)
        coach_profile_data = validated_data.pop('coach_profile', None)
        
        # Log basic changes (very naive comparison for brevity)
        old_position_id = instance.job_position_id
        old_status = instance.status

        # Update basic info
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Check differences for log
        changes = []
        if old_position_id != instance.job_position_id:
            changes.append(f"Position ID: {old_position_id} -> {instance.job_position_id}")
        if old_status != instance.status:
            changes.append(f"Status: {old_status} -> {instance.status}")

        if branch_assignments_data is not None:
            # Full replace strategy for simplicity
            instance.branch_assignments.all().delete()
            for item in branch_assignments_data:
                EmployeeBranchAssignment.objects.create(employee=instance, **item)
            changes.append("Branch assignments updated")

        if coach_profile_data is not None:
            if hasattr(instance, 'coach_profile'):
                for attr, value in coach_profile_data.items():
                    setattr(instance.coach_profile, attr, value)
                instance.coach_profile.save()
            else:
                CoachProfile.objects.create(employee=instance, **coach_profile_data)
            changes.append("Coach profile updated")

        if changes:
            request = self.context.get('request')
            user = request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None
            EmployeeHistory.objects.create(
                employee=instance,
                change_type='UPDATE_EMPLOYEE',
                new_value=", ".join(changes),
                changed_by=user
            )

        return instance
