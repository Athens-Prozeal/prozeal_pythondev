from rest_framework.permissions import BasePermission

from authentication.permissions import is_epc_admin_or_epc,is_client,is_quality_inspector,is_sub_contractor,is_safety_officer

def check_obj_permission(user, work_site, action: str, obj):
    if action == "retrieve":
        if obj.status == "submitted":
            if is_epc_admin_or_epc(user, work_site) or is_sub_contractor(
                user, work_site
            ):
                return True

        elif obj.status == "epc_approved":
            if (
                is_epc_admin_or_epc(user, work_site)
                or is_sub_contractor(user, work_site)
                or is_client(user, work_site)
            ):
                return True

        elif obj.status == "client_rejected":
            if (
                is_epc_admin_or_epc(user, work_site)
                or is_sub_contractor(user, work_site)
                or is_client(user, work_site)
            ):
                return True

        else:  # client_approved, closed and auto_closed
            if (
                is_epc_admin_or_epc(user, work_site)
                or is_client(user, work_site)
                or is_sub_contractor(user, work_site)
                or is_quality_inspector(user, work_site)
                or is_safety_officer(user, work_site)
            ):
                return True

    elif action == "destroy":
        if (obj.status == "submitted" or obj.status == "epc_approved") and (
            obj.submitted_by == user or is_epc_admin_or_epc(user, work_site)
        ):
            return True

    return False


class PTWPermission(BasePermission):
    def has_permission(self, request, view):
        "Update not allowed"
        user = request.user
        work_site = request.work_site

        if view.action == "create":
            if is_sub_contractor(user, work_site):
                return True

        if view.action == "list" or view.action == "retrieve":
            return True
        
        if view.action == "destroy":
            if is_epc_admin_or_epc(user, work_site) or is_sub_contractor(user, work_site):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, view.action, obj)


class PTWVerifyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site

        if is_epc_admin_or_epc(user, work_site):
            return True
        
        return False


class PTWClientApproveRejectPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site

        if is_client(user, work_site):
            return True

        return False
    

class PTWClosureRequestPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site

        if is_epc_admin_or_epc(user, work_site):
            return True

        return False
    

class PTWClosePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site

        if is_client(user, work_site):
            return True

        return False

