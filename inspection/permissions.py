from rest_framework.permissions import BasePermission

from authentication.permissions import is_epc_admin, is_epc_admin_or_epc, is_client, is_quality_inspector, is_sub_contractor

def check_obj_permission(user, work_site, action:str, obj):
    """ Update is not allowed, Approval is defined in a seperate view """
    if action == 'retrieve':
        if is_epc_admin(user):
            return True
        
        if obj.checked_by == user or obj.witness_1 == user or obj.witness_2 == user or obj.witness_3 == user:
            return True
    
        if obj.approval_status == 'approved': # Return as document on retieve
            if is_client(user, work_site) or is_epc_admin_or_epc(user, work_site) or is_sub_contractor(user, work_site) or is_quality_inspector(user, work_site): 
                return True

    if action == 'destroy':
        if is_epc_admin(user): # Master Admin has all access
            return True
        
        if obj.checked_by == user:
            return True
                
    return False


class InspectionPermission(BasePermission):
    def has_permission(self, request, view):
        """ Update  is not allowed, Approval is defined in a seperate view"""
        user = request.user
        work_site = request.work_site
        
        if view.action == 'create': 
            if is_epc_admin_or_epc(user, work_site) or is_quality_inspector(user, work_site):
                return True

        elif (view.action == 'list' or view.action == 'retrieve' or view.action == 'destroy'):
            is_client(user, work_site) or is_epc_admin_or_epc(user, work_site) or is_quality_inspector(user, work_site) or is_sub_contractor(user, work_site)
            return True  
        
        return False

    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, view.action, obj)



class InspectionApprovePermission(BasePermission):
    def has_permission(self, request, view):
        # All users can approve
        return True
    
