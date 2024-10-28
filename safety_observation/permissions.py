from rest_framework.permissions import BasePermission

from authentication.models import CorrectiveActionUser
from authentication.permissions import is_epc_admin, is_epc_admin_or_epc, is_client, is_sub_contractor, is_quality_inspector, is_safety_officer
from .models import SafetyObservation


def check_obj_permission(user, work_site, action:str,  obj:SafetyObservation):
    if is_epc_admin(user): # Master Admin has all access
        return True

    if action == 'retrieve': # Assigned to all
        if is_epc_admin_or_epc(user, work_site) or is_client(user, work_site)  or is_sub_contractor(user, work_site) or is_quality_inspector(user, work_site) or is_safety_officer(user, work_site):
            return True

    if action == 'destroy': 
        if obj.observation_status == 'open' and obj.reported_by == user:
            return True

    return False

class ObservationClassificationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site
        if is_epc_admin_or_epc(user, work_site) or is_safety_officer(user, work_site):
            return True
        
        return False

class SafetyObservationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site

        if (view.action == 'list' or view.action == 'retrieve'): 
            if (is_epc_admin_or_epc(request.user, request.work_site) or is_client(request.user, request.work_site)  or is_sub_contractor(request.user, request.work_site) 
                or is_quality_inspector(request.user, request.work_site)
                or is_safety_officer(request.user, request.work_site)
                ): 
                return True

        elif (view.action == 'create' or view.action == 'destroy'):
            
            if is_epc_admin_or_epc(user, work_site) or is_safety_officer(user, work_site):
                return True

        return False
    
    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, view.action, obj)


class CorrectiveActionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site
        corrective_action_users = CorrectiveActionUser.objects.get(work_site=work_site).users.all()
        if user in corrective_action_users:
            return True
        
        return False


class ReviewCorrectiveActionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site
            
        if is_epc_admin_or_epc(user, work_site) or is_safety_officer(user, work_site):
            return True
    
        return False

