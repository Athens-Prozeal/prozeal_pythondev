from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import WorkSiteRole

def has_work_site_role(user, work_site):
    """Checks if the user has any role for the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
    ).exists()


def is_epc_admin(user):
    """Checks if the user is the master admin (Software Purchased)."""
    return user.is_epc_admin


def is_client(user, work_site):
    """Checks if the user is a client of the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
        role='client'
    ).exists()


def is_epc(user, work_site):
    """Checks if the user is an EPC for the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
        role='epc'
    ).exists()


def is_sub_contractor(user, work_site):
    """Checks if the user is a sub contractor for the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
        role='sub_contractor'
    ).exists()


def is_quality_inspector(user, work_site):
    """Checks if the user is a quality inspector for the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
        role='quality_inspector'
    ).exists()   


def is_safety_officer(user, work_site):
    """Checks if the user is a safety officer for the work site."""
    return WorkSiteRole.objects.filter(
        user=user,
        work_site=work_site,
        role='safety_officer'
    ).exists()


def is_epc_admin_or_epc(user, work_site):
    """Checks if the user is a client or Sub Contractor for the work site."""
    return is_epc_admin(user) or is_epc(user, work_site)


def is_epc_or_sub_contractor(user, work_site):
    """Checks if the user is a client or Sub Contractor for the work site."""
    return is_epc(user, work_site) or is_sub_contractor(user, work_site)


def is_client_or_epc(user, work_site):
    """Checks if the user is a client or EPC for the work site."""
    return is_epc(user, work_site) or is_client(user, work_site)


def is_client_or_epc_or_sub_contractor(user, work_site):
    """Checks if the user is a client or EPC or Sub Contractor for the work site."""
    return is_client(user, work_site) or is_epc(user, work_site) or is_sub_contractor(user, work_site)


def is_client_or_epc_admin_or_epc_or_sub_contractor(user, work_site):
    """Checks if the user is a client or EPC or Sub Contractor for the work site."""
    return is_client(user, work_site) or is_epc_admin(user) or is_epc(user, work_site) or is_sub_contractor(user, work_site)


class HasWorkSitePermission(BasePermission):
    """
    Allows access only to users who have any role in the work site (WorkSiteRole).
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required.')
        
        if is_epc_admin(request.user): # Master Admin has access to all work sites  
            return True

        if WorkSiteRole.objects.filter(user=request.user, work_site = request.work_site).exists():
            return True

        return False


class IsClient(BasePermission):
    """
    Allows access only to clients of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_client(request.user, request.work_site):
            return True

        return False
    

class IsEPC(BasePermission):
    """
    Allows access only to EPCs of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_epc(request.user, request.work_site):
            return True

        return False
    

class IsSubContractor(BasePermission):
    """
    Allows access only to Sub Contractors of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_sub_contractor(request.user, request.work_site):
            return True

        return False
    
class IsEPCAdmin(BasePermission):
    """
    Allows access only to Master Admin
    """
    def has_permission(self, request, *args, **kwarsg):
        return is_epc_admin(request.user)


class IsClientOrEPC(BasePermission):
    """
    Allows access only to EPCs or Clients of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_client_or_epc(request.user, request.work_site):
            return True
        
        return False


class IsEPCOrEPCAdmin(BasePermission):
    """
    Allows access only to EPCs or EPC Admins of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_epc(request.user, request.work_site) or is_epc_admin(request.user):
            return True

        return False
    

class IsEPCOrEPCAdminOrQualityInspector(BasePermission):
    """
    Allows access only to EPCs or EPC Admins or Quality Inspectors of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_epc(request.user, request.work_site) or is_epc_admin(request.user) or is_quality_inspector(request.user, request.work_site):
            return True

        return False

class IsEpcOrEpcAdminOrSafetyOfficer(BasePermission):
    """
    Allows access only to EPCs or EPC Admins or Safety Officers of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_epc(request.user, request.work_site) or is_epc_admin(request.user) or is_safety_officer(request.user, request.work_site):
            return True

        return False


class IsClientOrEPCOrSubContractor(BasePermission):
    """
    Allows access only to EPCs or Clients or Sub Contractors of the requested work site.
    """
    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')

        if is_client_or_epc_or_sub_contractor(request.user, request.work_site):
            return True

        return False


class IsClientOrEPCAdminOrEPCOrSubContractor(BasePermission):
    """
    Allows access only to EPCs EPC Admin or Clients or Sub Contractors of the requested work site.
    """

    def has_permission(self, request, view):
        if not request.work_site:
            raise PermissionDenied('work_site_id is required in the request.')
        
        if is_client_or_epc_admin_or_epc_or_sub_contractor(request.user, request.work_site):
            return True

        return False
