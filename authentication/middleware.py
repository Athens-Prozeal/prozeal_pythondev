from django.shortcuts import get_object_or_404
from authentication.models import WorkSite

class WorkSiteMiddleware:
    """
    Extracts `work_site_id` from request query parameters and gets work_site and attaches to `request.work_site` 

    This ensures that subsequent views or middleware can rely on
    `request.work_site` to access the WorkSite associated with the request.

    **Permission checks are checked from this url parameter, So request.work_site SHOULD be used in 
    every cases
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        work_site = None
        work_site_id = request.GET.get('work_site_id')
        if work_site_id: # Some views may not require work_site, client should not pass incorrect work_site_id in that case
            work_site = get_object_or_404(WorkSite, id=work_site_id)

        request.work_site = work_site
        response = self.get_response(request)
        return response

