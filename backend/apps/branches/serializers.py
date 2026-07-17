from rest_framework import serializers
from .models import Branch

class BranchSerializer(serializers.ModelSerializer):
    pic_position = serializers.ReadOnlyField()
    pic_contact = serializers.ReadOnlyField()

    class Meta:
        model = Branch
        fields = [
            'id', 'code', 'name', 'short_name', 'branch_type', 'parent_branch', 'logo',
            'address', 'province', 'city', 'district', 'sub_district', 'postal_code', 'map_location',
            'whatsapp_number', 'email', 'person_in_charge', 'pic_position', 'pic_contact',
            'timezone', 'operational_date', 'status', 'status_effective_date', 'deactivation_reason', 'notes',
            'is_active', 'created_at', 'updated_at', 'version'
        ]
        read_only_fields = ['pic_position', 'pic_contact', 'is_active', 'created_at', 'updated_at', 'version']

from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'branch', 'branch_name', 'code', 'name', 'room_type', 
            'capacity_ideal', 'capacity_max', 'facilities', 'status', 'notes',
            'is_active', 'created_at', 'updated_at', 'version'
        ]


from .models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Holiday
        fields = '__all__'
