from django.contrib.auth import get_user_model

from authentication.models import WorkSiteRole

User = get_user_model()

def get_users_in_role(work_site, role:str):
    """ Gets all users in a role at a worksite. """
    work_site_roles = WorkSiteRole.objects.filter(work_site=work_site, role=role)
    users = User.objects.filter(work_site_roles__in=work_site_roles)

    return users
