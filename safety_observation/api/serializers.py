from rest_framework import serializers
from rest_framework.serializers import ValidationError

from safety_observation.models import SafetyObservation
from safety_observation.permissions import check_obj_permission
from authentication.models import CorrectiveActionUser


class SafetyObservationSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    sub_contractor_full_name = serializers.CharField(source='sub_contractor.full_name', read_only=True)
    reported_by_full_name = serializers.CharField(source='reported_by.full_name', read_only=True)
    corrective_action_assigned_to_full_name = serializers.CharField(source='corrective_action_assigned_to.full_name', read_only=True)

    class Meta:
        model = SafetyObservation
        read_only_fields = ('closed_on', 'reported_by_full_name', 'sub_contractor_full_name', 'corrective_action_assigned_to_full_name', 'status',)
        exclude = ('reported_by', 'work_site', 'created_by', 'last_updated_by', 'created_at', 'last_updated_at',)

    def validate(self, attrs):
        request = self.context["request"]
        work_site = request.work_site
        reported_by = request.user
        observation_status = attrs.get("observation_status")
        corrective_action_assigned_to = attrs.get("corrective_action_assigned_to")
        department = attrs.get("department")

        if department not in request.user.departments.all():
            raise ValidationError('Invalid Department') 
        
        if corrective_action_assigned_to not in CorrectiveActionUser.objects.get(work_site=work_site).users.all():
            raise ValidationError('Invalid Corrective Action User')

        if reported_by == corrective_action_assigned_to:
            raise ValidationError('Reported by and Corrective Action Assigned to should be different')

        if observation_status == 'closed':
            if not attrs.get("after_image"):
                raise ValidationError('After image is required for closed observation')

            if not attrs.get('corrective_action_taken'):
                raise ValidationError('Corrective Action Taken is required for closed observation')

        return super().validate(attrs)

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context["request"].user
        work_site = self.context["request"].work_site
        work_site_id = work_site.id

        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/safety-observation/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/safety-observation/{instance.id}/?work_site_id={work_site_id}",
            },
            "corrective_action": {
                "name": "corrective_action",
                "method": "PUT",
                "url": f"/api/safety-observation/{instance.id}/corrective-action/?work_site_id={work_site_id}",
            },
            "verify": {
                "name": "verify",
                "method": "PUT",
                "url": f"/api/safety-observation/{instance.id}/verify/?work_site_id={work_site_id}",
            },
            "reject": {
                "name": "reject",
                "method": "PUT",
                "url": f"/api/safety-observation/{instance.id}/reject/?work_site_id={work_site_id}",
            }
        }

        allowed_actions = []

        if check_obj_permission(user, work_site, "retrieve", instance):
            allowed_actions.append(actions["view"])
            
        if check_obj_permission(user, work_site, "destroy", instance):
            allowed_actions.append(actions["delete"])

        if instance.status == 'open' and instance.corrective_action_assigned_to == user:
            allowed_actions.append(actions["corrective_action"])

        if instance.status == 'verification_required' and instance.reported_by == user:
            allowed_actions.append(actions['verify'])
            allowed_actions.append(actions['reject'])

        data["actions"] = allowed_actions

        return data

