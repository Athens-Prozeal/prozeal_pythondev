from rest_framework import serializers
from django.contrib.auth import get_user_model

from authentication.models import WorkSiteRole, WorkSite
from authentication.permissions import is_epc_admin
from authentication.models import Department

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            msg = 'Username and Password requried.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['username'] = username
        attrs['password'] = password
        return attrs


class WorkSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSite
        fields = ("id", "name")


class WorkSiteRoleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='work_site.id')
    name = serializers.CharField(source='work_site.name')
    display_role = serializers.CharField(source='get_role_display')

    class Meta:
        model = WorkSiteRole
        fields = ('id', 'name', 'role', 'display_role')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the user detail. Strictly to be used for read only.
    """
    work_site_roles = WorkSiteRoleSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_active', 'email', 'first_name', 'last_name', 'company', 'work_site_roles',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
        user = request.user
        allowed_actions = []
        role = None
        
        if is_epc_admin(user):
            actions = {
                "edit": {
                    "name": "edit",
                    "method": "PUT",
                    "url": f"/api/auth/user-role/{instance}/",
                },
            }
            data['id'] = instance.id
            allowed_actions.append(actions['edit'])
        
        if request.work_site:
            role = WorkSiteRole.objects.get(user=instance, work_site=request.work_site).role
        
        data['actions']  =  allowed_actions
        data['role'] = role 

        return data
    
class SubContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class WitnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'company') 


class QualityEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'company') 


class ExecutionEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'company') 


class CorrectiveActionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

