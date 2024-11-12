from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import HasWorkSitePermission
from tbt.permissions import ToolBoxTalkPermission
from tbt.models import ToolBoxTalk
from .serializers import ToolBoxTalkSerializer


class TbtViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, ToolBoxTalkPermission]
    serializer_class = ToolBoxTalkSerializer

    def get_queryset(self):
        work_site = self.request.work_site
        return ToolBoxTalk.objects.filter(work_site=work_site)

    def perform_create(self, serializer):
        work_site = self.request.work_site
        serializer.save(
            work_site = work_site,
            created_by=self.request.user,
            last_updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            last_updated_by=self.request.user
        )
    
    def perform_partial_update(self, serializer):
        serializer.save(
            last_updated_by=self.request.user
        )

    def perform_destroy(self, instance):
        instance.delete()

