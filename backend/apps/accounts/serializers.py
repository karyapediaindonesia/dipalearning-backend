from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, Permission

User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), source='permissions', write_only=True, many=True, required=False
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'permission_ids']

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='roles', write_only=True, many=True, required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'roles', 'role_ids', 'assigned_branches', 'is_locked', 'photo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        assigned_branches = validated_data.pop('assigned_branches', [])
        user = User.objects.create_user(**validated_data)
        if roles:
            user.roles.set(roles)
        if assigned_branches:
            user.assigned_branches.set(assigned_branches)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Check if user exists using username or email
            user_obj = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()
            
            if user_obj:
                if user_obj.is_locked:
                    raise serializers.ValidationError("Account is locked due to multiple failed login attempts.")
                
                user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
                if not user:
                    user_obj.failed_login_attempts += 1
                    if user_obj.failed_login_attempts >= 3:
                        user_obj.is_locked = True
                    user_obj.save()
                    raise serializers.ValidationError("Invalid credentials.")
                
                # Reset attempts on success
                user.failed_login_attempts = 0
                user.is_locked = False
                user.save()
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data
