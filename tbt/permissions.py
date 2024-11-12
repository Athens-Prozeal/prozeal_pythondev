from rest_framework.permissions import BasePermission

from authentication.permissions import is_epc, is_epc_admin, is_client, is_sub_contractor, is_quality_inspector


def check_obj_permission(user, work_site, action:str,  obj=None):
    if is_epc_admin(user): # Master Admin has all access
        return True
    
    if action == 'retrieve':
        if is_epc(user, work_site) or is_client(user, work_site)  or is_sub_contractor(user, work_site) or is_quality_inspector(user, work_site):
            return True
    
    if action == 'update' or action == 'partial_update' or action == 'destroy':
        if is_epc(user, work_site):
            return True

    return False


class ToolBoxTalkPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site
        if is_epc_admin(user): # Master Admin has all access
            return True

        if (view.action == 'list' or 
            view.action == 'retrieve'): 
            if is_epc(user, work_site) or is_client(user, work_site)  or is_sub_contractor(user, work_site) or is_quality_inspector(user, work_site): 
                return True  
        
        elif (view.action == 'create' or 
              view.action == 'update' or 
              view.action == 'partial_update' or
              view.action == 'destroy'):
            if is_epc(user, work_site):
                return True
    
        return False

    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, view.action, obj)

