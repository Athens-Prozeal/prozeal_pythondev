from rest_framework import serializers

from worker.models import Worker
from worker.permissions import check_obj_permission

class WorkerSerializer(serializers.ModelSerializer):
    created_under = serializers.CharField(source='created_under.username', required=False)

    class Meta:
        model = Worker
        read_only_fields = ("created_under",)
        exclude = ["work_site", "created_by", "last_updated_by", "created_at", "last_updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context["request"]
        user = request.user
        work_site = request.work_site
        work_site_id = work_site.id 

        if user == instance.created_under:
            data['created_under'] = 'Me'        

        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/worker/{instance.id}/?work_site_id={work_site_id}",
            },
            "edit": {
                "name": "edit",
                "method": "PUT",
                "url": f"/api/worker/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/worker/{instance.id}/?work_site_id={work_site_id}",
            }
        }

        allowed_actions = []

        if check_obj_permission(user, work_site, instance, "retrieve" ):
            allowed_actions.append(actions["view"])
        
        if check_obj_permission(user, work_site, instance, "update"):
            allowed_actions.append(actions["edit"])
        
        if check_obj_permission(user, work_site, instance, "destroy"):
            allowed_actions.append(actions["delete"])

        data["actions"] = allowed_actions
        return data

