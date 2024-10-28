from rest_framework.permissions import BasePermission

from authentication.permissions import is_epc, is_epc_admin, is_sub_contractor, is_client, is_client_or_epc_or_sub_contractor
from .models import Worker

def check_obj_permission(user, work_site, obj:Worker, action):
    if is_epc_admin(user): # Master Admin has all access except client's worker
        if not is_client(obj.created_under, work_site): # worker doesn't belong to client
            return True
    
    elif is_client(user, work_site):
        if action == 'retrieve': # client can view all workers
            return True
        
        elif action == 'update' or action == 'partial_update' or action == 'destroy':
            if is_client(obj.created_under, work_site):
                return True
            
    elif is_epc(user, work_site): # Update it with Or quality inspector
        if not is_client(obj.created_under, work_site): # worker doesn't belong to client
            return True

    elif is_sub_contractor(user, work_site):
        if obj.created_under == user: # have permission to only their own workers
            return True

    return False

class WorkerPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if is_epc_admin(user):
            return True
        
        if is_client_or_epc_or_sub_contractor(user, request.work_site): # Also allow quality inspector to hve view access
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, obj, view.action)

