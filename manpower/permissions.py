from rest_framework.permissions import BasePermission

from authentication.permissions import is_epc_admin, is_epc, is_epc_admin_or_epc, is_client, is_sub_contractor, is_epc_or_sub_contractor

def check_obj_permission(user, work_site, obj, action:str):
    if is_epc_admin(user): # Master Admin has all access
        return True
    
    if is_client(user, work_site):
        # No object permission for client
        pass

    if is_epc(user, work_site):
        return True
    
    if is_sub_contractor(user, work_site):
        if obj.sub_contractor == user: # Sub Contractor can only edit their own manpower
            if action == 'retrieve':
                return True
            elif action == 'update' or action == 'destroy':
                """Sub Contractor can only update or delete if the manpower is not verified
                ** Do not allow sub_contractor to edit varification_status field
                """
                if obj.verification_status == 'Not Verified' or obj.verification_status == 'Revise':
                    return True                
    return False


class ManpowerPermission(BasePermission):
    def has_permission(self, request, view):
        """
        General manpower permission, field level permisisons for verification_status, verified_by etc 
        are to be handled in the serializer or views
        """
        user = request.user
        if is_epc_admin(user):
            return True

        if is_client(user, request.work_site): # Add quality inspector to list and retrieve 
            if view.action == "list" or view.action == "retrieve":
                # return queryset of only verified manpowers in views
                return True

        if is_epc_or_sub_contractor(user, request.work_site):
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        return check_obj_permission(request.user, request.work_site, obj, view.action)
    

class ManpowerStatusPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        work_site = request.work_site
        if is_epc_admin_or_epc(user , work_site):
            return True

        return False

