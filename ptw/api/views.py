from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from authentication.permissions import (HasWorkSitePermission, is_epc_admin_or_epc, is_client, is_sub_contractor, is_quality_inspector, is_safety_officer)
from ptw.models import General, BasePermitToWork
from .serializers import GeneralSubmitSerializer
from ptw.permissions import PTWPermission, PTWVerifyPermission, PTWClientApproveRejectPermission, PTWClosureRequestPermission, PTWClosePermission


class BaseEPCVerify(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWVerifyPermission]

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        signature = request.data.get("signature")
        ptw = get_object_or_404(self.model, id=pk, work_site=request.work_site)
        datetime = timezone.now()

        if ptw.status == "submitted":
            ptw.status = "epc_approved"
            ptw.verified_by = user
            ptw.verified_datetime = datetime
            ptw.verified_by_signature = signature

        else:
            return Response({"message": "Invalid request."}, status=400)

        ptw.last_updated_by = user
        ptw.save()
        return Response({"message": "PTW approved successfully."})
    

class BaseClientApprove(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWClientApproveRejectPermission]

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        signature = request.data.get("signature")
        ptw = get_object_or_404(self.model, id=pk, work_site=request.work_site)
        datetime = timezone.now()

        if ptw.status == "epc_approved":
            ptw.status = "client_approved"
            ptw.approved_by = user
            ptw.approved_datetime = datetime
            ptw.issued_date = datetime
            ptw.approved_by_signature = signature

        else:
            return Response({"message": "Invalid request."}, status=400)

        ptw.last_updated_by = user
        ptw.save()
        return Response({"message": "PTW approved successfully."})


class BaseClientReject(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWClientApproveRejectPermission]

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        ptw = get_object_or_404(self.model, id=pk, work_site=request.work_site)
        rejected_remark = request.data.get("rejected_remark")

        if ptw.status == "epc_approved":
            ptw.status = "client_rejected"
            ptw.rejected_by = user
            ptw.rejected_remark = rejected_remark

        else:
            return Response({"message": "Invalid request."}, status=400)

        ptw.last_updated_by = user
        ptw.save()
        return Response({"message": "PTW rejected"})


class BaseClosureRequest(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWClosureRequestPermission]

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        ptw = get_object_or_404(self.model, id=pk, work_site=request.work_site)
        
        if ptw.status == "client_approved":
            ptw.closure_requested_by = user
            ptw.closure_requested_at = timezone.now()
        
        else:
            return Response({"message": "Invalid request."}, status=400)

        ptw.last_updated_by = user 
        ptw.save()
        return Response({"message": "Closure request submitted."})


class BaseClose(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWClosePermission]

    def put(self, request, pk, *args, **kwargs):
        user = request.user
        ptw = get_object_or_404(self.model, id=pk, work_site=request.work_site)
        
        if ptw.status == "client_approved" and ptw.closure_requested_by:
            ptw.status = "closed"
            ptw.closure_accepted_by = user
            ptw.closed_at = timezone.now()
        
        else:   
            return Response({"message": "Invalid request."}, status=400)

        ptw.last_updated_by = user 
        ptw.save()
        return Response({"message": "PTW closed."})



def update_expired_ptws(ptw_model:BasePermitToWork, work_site):
    ptws = ptw_model.objects.filter(work_site=work_site)

    expired_ptws = ptws.filter(validity__lte=timezone.now())

    to_auto_close = expired_ptws.filter(status='client_approved')
    to_expire = expired_ptws.filter(status__in=[
        'submitted', 'epc_approved', 'client_rejected'
    ])

    with transaction.atomic():
        to_auto_close.update(status='auto_closed')
        to_expire.update(status='expired')


class GeneralPtwViewSet(viewsets.ModelViewSet):
    "Update, Delete not allowed"
    permission_classes = [IsAuthenticated, HasWorkSitePermission, PTWPermission]
    serializer_class = GeneralSubmitSerializer

    def get_queryset(self):
        work_site = self.request.work_site
        update_expired_ptws(General, work_site)
        return General.objects.filter(work_site=work_site)

    def list(self, request, *args, **kwargs):
        work_site = self.request.work_site
        user = self.request.user
        ptw_status = self.request.query_params.get("status")
        update_expired_ptws(General, work_site)

        ptws = General.objects.filter(work_site=work_site)

        # Define the role conditions for each status
        role_conditions = {
            "open": lambda user, ws: is_epc_admin_or_epc(user, ws) or is_client(user, ws) or is_sub_contractor(user, ws) or is_quality_inspector(user, ws) or is_safety_officer(user, ws),
            "closed": lambda user, ws: is_epc_admin_or_epc(user, ws) or is_client(user, ws) or is_sub_contractor(user, ws) or is_quality_inspector(user, ws) or is_safety_officer(user, ws),
            "submitted": lambda user, ws: is_epc_admin_or_epc(user, ws) or is_sub_contractor(user, ws),
            "pending-approval": lambda user, ws: is_client(user, ws) or is_epc_admin_or_epc(user, ws) or is_sub_contractor(user, ws),
            "rejected": lambda user, ws: is_client(user, ws) or is_epc_admin_or_epc(user, ws) or is_sub_contractor(user, ws),
            "expired": lambda user, ws: is_epc_admin_or_epc(user, ws) or is_client(user, ws) or is_sub_contractor(user, ws) 
        }

        status_mapping = {
            "open": "client_approved",
            "closed": "closed",
            "submitted": "submitted",
            "pending-approval": "epc_approved",
            "rejected": "client_rejected",
            "expired": "expired"
        }

        if ptw_status in role_conditions and role_conditions[ptw_status](user, work_site):
            if ptw_status == 'closed':
                ptws = ptws.filter(status__in=['closed', 'auto_closed'])
            else:
                ptws = ptws.filter(status=status_mapping[ptw_status])
  
        else:
            ptws = ptws.none()

        serializer = self.get_serializer(ptws, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        work_site = self.request.work_site
        status = "submitted"

        serializer.save(
            submitted_by=self.request.user,
            status=status,
            work_site=work_site,
            created_by=self.request.user,
            last_updated_by=self.request.user,
        )

    def perform_destroy(self, instance):
        instance.delete()


class VerifyGeneralPtw(BaseEPCVerify):
    model = General


class ClientApproveGeneralPtw(BaseClientApprove):
    model = General


class ClientRejectGeneralPtw(BaseClientReject):
    model = General


class ClosureRequestGeneralPtw(BaseClosureRequest):
    model = General


class CloseGeneralPtw(BaseClose):
    model = General


