from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.selectors import get_users_in_role

from authentication.permissions import HasWorkSitePermission, is_client, is_epc_admin_or_epc, is_sub_contractor
from worker.permissions import WorkerPermission
from .serializers import WorkerSerializer
from worker.models import Worker

class WorkerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, WorkerPermission]
    serializer_class = WorkerSerializer

    def get_queryset(self):
        work_site = self.request.work_site
        user = self.request.user

        client_users = get_users_in_role(work_site, "client")

        if is_client(user, work_site):
            return Worker.objects.filter(work_site=work_site)
        
        elif is_epc_admin_or_epc(user, work_site):
            return Worker.objects.filter(work_site=work_site).exclude(created_under__in=client_users)
        
        elif is_sub_contractor(user, work_site.id):
            return Worker.objects.filter(work_site=work_site, created_under=user)
        
        return Worker.objects.none()
    
    def perform_create(self, serializer):
        work_site = self.request.work_site
        serializer.save(
            work_site = work_site,
            created_by=self.request.user,
            created_under=self.request.user,
            last_updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            last_updated_by=self.request.user
        )

    def perform_partial_update(self, serializer):
        print("serializer.validated_data")
        print(serializer.validated_data)
        serializer.save(
            last_updated_by=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.delete()
