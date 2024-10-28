from rest_framework import serializers

from tbt.models import ToolBoxTalk
from tbt.permissions import check_obj_permission


class ToolBoxTalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolBoxTalk
        exclude = ('work_site', 'created_by', 'last_updated_by', 'created_at', 'last_updated_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        work_site = self.context['request'].work_site
        work_site_id = work_site.id

        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/tbt/{instance.id}/?work_site_id={work_site_id}",
            },
            "edit": {
                "name": "edit",
                "method": "PUT",
                "url": f"/api/tbt/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/tbt/{instance.id}/?work_site_id={work_site_id}",
            }
        }

        allowed_actions = []

        if check_obj_permission(user, work_site, "retrieve", instance):
            allowed_actions.append(actions["view"])
        
        if check_obj_permission(user, work_site, "update", instance):
            allowed_actions.append(actions["edit"])
        
        if check_obj_permission(user, work_site, "destroy", instance):
            allowed_actions.append(actions["delete"])

        data["actions"] = allowed_actions
        return data

