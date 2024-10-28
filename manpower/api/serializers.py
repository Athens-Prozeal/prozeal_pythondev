from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from django.contrib.auth import get_user_model

from authentication.permissions import is_epc_admin_or_epc, is_sub_contractor
from manpower.permissions import check_obj_permission
from manpower.models import Manpower

User = get_user_model()


class ManpowerSerializer(ModelSerializer):
    sub_contractor_username = CharField(
        source="sub_contractor.username", required=False, read_only=True
    )
    verified_by = CharField(source="verified_by.username", required=False)

    class Meta:
        model = Manpower
        exclude = (
            "work_site",
            "created_by",
            "last_updated_by",
            "created_at",
            "last_updated_at",
        )
        extra_kwargs = {"sub_contractor": {"required": False}}

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user
        work_site = request.work_site

        if request.method == "POST":
            if is_sub_contractor(user, work_site):
                attrs["sub_contractor"] = user

            if Manpower.objects.filter(
                work_site=work_site, date=attrs.get("date"), sub_contractor=attrs.get("sub_contractor")
            ).exists():
                raise ValidationError("Manpower report for this date already exists.")

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
                "url": f"/api/manpower/{instance.id}/?work_site_id={work_site_id}",
            },
            "edit": {
                "name": "edit",
                "method": "PUT",
                "url": f"/api/manpower/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/manpower/{instance.id}/?work_site_id={work_site_id}",
            },
            "update_status": {
                "name": "update_status",
                "method": "PUT",
                "url": f"/api/manpower/{instance.id}/update-status/?work_site_id={work_site_id}",
                "statuses": ["Verified", "Revise", "Not Verified"],
            },
        }

        allowed_actions = []

        if check_obj_permission(user, work_site, instance, "retrieve"):
            allowed_actions.append(actions["view"])

        if check_obj_permission(user, work_site, instance, "update"):
            allowed_actions.append(actions["edit"])

        if check_obj_permission(user, work_site, instance, "destroy"):
            allowed_actions.append(actions["delete"])

        if is_epc_admin_or_epc(user, work_site):
            allowed_actions.append(actions["update_status"])

        data["actions"] = allowed_actions

        return data


class ManpowerStatusSerializer(ModelSerializer):
    verified_by = CharField(source="verified_by.username", required=False)

    class Meta:
        model = Manpower
        fields = ("verification_status", "verified_by", )


class ManpowerReportSerializer(ModelSerializer):
    class Meta:
        model = Manpower
        fields = ("date", "number_of_workers", )

