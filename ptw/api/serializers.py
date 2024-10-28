from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth import get_user_model

from authentication.permissions import is_epc_admin_or_epc, is_client
from ptw.models import General
from ptw.permissions import check_obj_permission

User = get_user_model()

class PTWBaseSubmitSerializer(ModelSerializer):
    submitted_by_username = CharField(source='submitted_by.username', required=False, read_only=True)
    verified_by_username = CharField(source='verified_by.username', required=False, read_only=True)
    approved_by_username = CharField(source='approved_by.username', required=False, read_only=True)
    rejected_by_username = CharField(source='rejected_by.username', required=False, read_only=True)
    closure_requested_by_username = CharField(source='closure_requested_by.username', required=False, read_only=True)
    closure_accepted_by_username = CharField(source='closure_accepted_by.username', required=False, read_only=True)
    work_site_name = CharField(source='work_site.name', required=False, read_only=True)

    read_only_fields = ('work_site', 'permit_no', 'issued_date', 'status', 'submitted_datetime', 'verified_datetime', 'verified_by_signature', 'approved_datetime', 'approved_by_signature', 'rejected_remark', 'closure_requested_at', 'closed_at')
    exclude = ('submitted_by', 'verified_by', 'approved_by', 'rejected_by', 'work_site', 'created_by', 'closure_requested_by', 'closure_accepted_by', 'last_updated_by', 'created_at', 'last_updated_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        work_site = self.context['request'].work_site
        work_site_id = work_site.id

        closure_requested = instance.closure_requested  
        
        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "verify": {
                "name": "verify",
                "method": "PUT",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/verify/?work_site_id={work_site_id}",
            },
            "client_approve": {
                "name": "client_approve",
                "method": "PUT",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/client-approve/?work_site_id={work_site_id}",
            },
            "client_reject": {
                "name": "client_reject",
                "method": "PUT",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/client-reject/?work_site_id={work_site_id}",
            },
            "closure_request": {
                "name": "closure_request",
                "method": "PUT",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/closure-request/?work_site_id={work_site_id}",
            },
            "close": {
                "name": "close",
                "method": "PUT",
                "url": f"/api/ptw/{instance.table_identifier}/{instance.id}/close/?work_site_id={work_site_id}",
            }
        }

        allowed_actions = []    

        if check_obj_permission(user, work_site, 'retrieve', instance):
            allowed_actions.append(actions["view"])
        
        if check_obj_permission(user, work_site, "destroy", instance):
            allowed_actions.append(actions["delete"])
            
        if instance.status == 'submitted' and is_epc_admin_or_epc(user, work_site):
            allowed_actions.append(actions["verify"])

        if instance.status == 'epc_approved' and is_client(user, work_site):
            allowed_actions.append(actions["client_approve"])
            allowed_actions.append(actions["client_reject"])

        if instance.status == 'client_approved' and is_epc_admin_or_epc(user, work_site) and not closure_requested:
            allowed_actions.append(actions["closure_request"])

        if instance.closure_requested_by and  is_client(user, work_site) and not instance.status == 'closed':
            allowed_actions.append(actions["close"])

        data["actions"] = allowed_actions
        data["closure_requested"] = closure_requested

        return data

class GeneralSubmitSerializer(PTWBaseSubmitSerializer):
    class Meta:
        model = General
        read_only_fields = PTWBaseSubmitSerializer.read_only_fields
        exclude = PTWBaseSubmitSerializer.exclude

