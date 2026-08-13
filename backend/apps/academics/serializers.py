
from rest_framework import serializers
from .models import Course, Level, Package, AcademicYear, AcademicPeriod, BranchAcademicPeriod, StudyClass

class LevelSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    prerequisite_name = serializers.CharField(source='prerequisite.name', read_only=True)
    order = serializers.IntegerField(required=False)
    
    class Meta:
        model = Level
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'category', 'learning_type', 'learning_mode',
            'default_duration', 'status', 'notes', 'levels',
            'is_active', 'created_at', 'updated_at', 'version'
        ]



class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class BranchAcademicPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchAcademicPeriod
        fields = ['branch', 'status']

class AcademicPeriodSerializer(serializers.ModelSerializer):
    branch_assignments = BranchAcademicPeriodSerializer(many=True, required=False)
    sequence = serializers.IntegerField(required=False)

    class Meta:
        model = AcademicPeriod
        fields = '__all__'

    def create(self, validated_data):
        branch_data = validated_data.pop('branch_assignments', [])
        period = AcademicPeriod.objects.create(**validated_data)
        
        if not period.is_global:
            for bd in branch_data:
                BranchAcademicPeriod.objects.create(academic_period=period, **bd)
                
        return period

    def update(self, instance, validated_data):
        branch_data = validated_data.pop('branch_assignments', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if branch_data is not None:
            instance.branch_assignments.all().delete()
            if not instance.is_global:
                for bd in branch_data:
                    BranchAcademicPeriod.objects.create(academic_period=instance, **bd)

        return instance

class StudyClassSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    coach_name = serializers.CharField(source='coach.full_name', read_only=True)

    class Meta:
        model = StudyClass
        fields = '__all__'
