from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from authentication.permissions import HasWorkSitePermission, IsClientOrEPCAdminOrEPCOrSubContractor, is_epc_admin_or_epc, is_client, is_sub_contractor
from manpower.permissions import ManpowerPermission, check_obj_permission, ManpowerStatusPermission
from manpower.models import Manpower
from .serializers import ManpowerSerializer, ManpowerStatusSerializer, ManpowerReportSerializer

User = get_user_model()

class ManpowerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, ManpowerPermission]
    serializer_class = ManpowerSerializer

    def get_queryset(self):
        work_site = self.request.work_site
        user = self.request.user

        if is_epc_admin_or_epc(user, work_site):
            return Manpower.objects.filter(work_site=work_site)
        
        elif is_client(user, work_site):
            return Manpower.objects.filter(work_site=work_site, verification_status='Verified')

        elif is_sub_contractor(user, work_site):
            return Manpower.objects.filter(work_site=work_site, sub_contractor=user)
        
        return Manpower.objects.none()
    
    def perform_create(self, serializer):
        """Only EPC, EPC admin and Sub contractor should create manpower"""
        work_site = self.request.work_site
        user = self.request.user
        data = serializer.validated_data

        if is_sub_contractor(user, work_site):
            # Sub contractor attribute is set in serializer validate() method
            data['verification_status'] = 'Not Verified'
            data['verified_by'] = None
        
        if data['verification_status'] == 'Verified':
            data['verified_by'] = user # by EPC admin or EPC

        serializer.save(
            work_site=work_site,
            created_by=user,
            last_updated_by=user,
        )

    def perform_update(self, serializer):
        """Only EPC, EPC admin and Sub contractor should be allowed to perform update"""
        work_site = self.request.work_site
        user = self.request.user
        data = serializer.validated_data

        if is_sub_contractor(user, work_site):
            data['sub_contractor'] = user
            data['verification_status'] = 'Not Verified'
            data['verified_by'] = None

        if data['verification_status'] == 'Verified':
            data['verified_by'] = user # Data by EPC admin or EPC
        else:
            data['verified_by'] = None

        serializer.save(
            last_updated_by=user,
        )

    def perform_destroy(self, instance):
        """Permission is checked in the permission class"""
        instance.delete()


class UpdateManpowerStatus(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, ManpowerStatusPermission]
    serializer = ManpowerStatusSerializer

    def put(self, request, pk):
        manpower = get_object_or_404(Manpower, id=pk)
        if check_obj_permission(request.user, request.work_site, manpower, 'update'):
            serializer = self.serializer(data=request.data)

            if serializer.is_valid():
                manpower.verification_status = serializer.validated_data['verification_status']
                if serializer.validated_data['verification_status'] == 'Verified':
                    manpower.verified_by = request.user
                else:
                    manpower.verified_by = None

                manpower.last_updated_by = request.user
                manpower.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
        return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)


class ManpowerStatistics(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsClientOrEPCAdminOrEPCOrSubContractor,]

    def get(self, request, *args, **kwargs):
        month = request.query_params.get("month", None)
        year = request.query_params.get("year", None)

        manpower_reports = Manpower.objects.filter(
        date__month=month,
        date__year=year,
        verification_status='Verified',
        work_site=request.work_site
        )

        if is_sub_contractor(request.user, request.work_site):
            manpower_reports = manpower_reports.filter(sub_contractor=request.user)

        users = User.objects.filter(
            manpower_reports__in=manpower_reports
        ).distinct().prefetch_related('manpower_reports')

        data = []
        for user in users:
            user_reports = manpower_reports.filter(sub_contractor=user)
            user_data = {
                "sub_contractor": user.username,
                "report": ManpowerReportSerializer(user_reports, many=True).data
            }
            data.append(user_data)

        return Response(data)

