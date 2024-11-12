from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.serializers import Serializer, CharField
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model 

from .serializers import LoginSerializer, UserSerializer, DepartmentSerializer, WorkSiteRoleSerializer, SubContractorSerializer, WorkSiteSerializer, WitnessSerializer, QualityEngineerSerializer, ExecutionEngineerSerializer, CorrectiveActionUserSerializer
from authentication.permissions import HasWorkSitePermission, IsEPCAdmin, IsEPCOrEPCAdmin, IsEPCOrEPCAdminOrQualityInspector, IsEpcOrEpcAdminOrSafetyOfficer
from authentication.models import WorkSiteRole, WorkSite, CorrectiveActionUser
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)

        login(request, user)
        serializer = UserSerializer(user, context={'request':request})
        return Response(serializer.data, status=200)

class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated]

    class UpdatePasswordSerializer(Serializer):
        old_password = CharField(required=True)
        new_password = CharField(required=True)

        class Meta:
            fields = ['old_password', 'new_password']

    def post(self, request):
        serializer = self.UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        try:
            validate_password(new_password, user=user)
        except Exception as e:
            return Response({"detail": e}, status=400)

        if not user.check_password(old_password):
            return Response({"detail": ["Invalid old password"]}, status=400)
        
        user.set_password(new_password)
        user.save()
        
        return Response({"detail": "Password updated successfully"}, status=200)


class LogOutUser(APIView):
    """
    Log out for session authentication.
    """
    def post(self, request):
        logout(request)
        return Response({'detail':'Log Out Successfull'}, status=204)


class GetMyUserDetail(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request':request})
        return Response(serializer.data)


class GetMyDepartments(ListAPIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        return user.departments.all()


class GetMyWorkSiteRole(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission]

    def get(self, request):
        work_site_role = WorkSiteRole.objects.get(user=request.user, work_site=request.work_site)
        serializer = WorkSiteRoleSerializer(work_site_role, context={'request':request})
        return Response(serializer.data)


class GetSubContractors(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsEPCOrEPCAdmin]

    def get(self, request):
        sub_contractors = User.objects.filter(work_site_roles__work_site=request.work_site, work_site_roles__role='sub_contractor').exclude(is_active=False)
        serilaizer = SubContractorSerializer(sub_contractors, many=True)
        return Response(serilaizer.data)


class GetWitnesses(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsEPCOrEPCAdminOrQualityInspector]

    def get(self, request):
        witnesses = User.objects.filter(work_site_roles__work_site=request.work_site).exclude(id=request.user.id).exclude(is_active=False)
        serilaizer = WitnessSerializer(witnesses, many=True)
        return Response(serilaizer.data)
    

class GetQualityEngineers(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsEPCOrEPCAdminOrQualityInspector]

    def get(self, request):
        quality_engineers = User.objects.filter(work_site_roles__work_site=request.work_site).exclude(id=request.user.id).exclude(is_active=False)
        serilaizer = QualityEngineerSerializer(quality_engineers, many=True)
        return Response(serilaizer.data)
    
class GetExecutionEngineers(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsEPCOrEPCAdminOrQualityInspector]

    def get(self, request):
        execution_engineers = User.objects.filter(work_site_roles__work_site=request.work_site).exclude(id=request.user.id).exclude(is_active=False)
        serilaizer = ExecutionEngineerSerializer(execution_engineers, many=True)
        return Response(serilaizer.data)


class GetCorrectiveActionUsers(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, IsEpcOrEpcAdminOrSafetyOfficer]
    serializer_class = CorrectiveActionUserSerializer

    def get(self, request):
        users = get_object_or_404(CorrectiveActionUser, work_site=request.work_site).users.all()
        serilaizer = CorrectiveActionUserSerializer(users, many=True)
        return Response(serilaizer.data)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEPCAdmin]
    serializer_class = UserSerializer

    def get(self, request):
        work_site = request.work_site
        if not work_site:
            users = User.objects.all()
        else:
            users = User.objects.filter(work_site_roles__work_site=work_site)
        users = users.exclude(is_superuser=True)
        serializer = UserSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)
    
    def post(self, request):
        request = self.request
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            company=data['company'],
            is_active=data['is_active']
        )
        user.set_password(data['password'])
        user.save()

        work_site_roles = request.data['work_site_roles']
        for work_site_role in work_site_roles:
            role = work_site_role['role']

            if role == 'epc_admin':
                return Response({"detail": "Only superuser can create EPC Admin"}, status=400)

            work_site = WorkSite.objects.get(id=work_site_role['id'])

            try:
                WorkSiteRole.objects.get(work_site=work_site, user=user, role=role)
                return Response({"detail": "Work site role already exists"}, status=400)
            except WorkSiteRole.DoesNotExist:
                WorkSiteRole.objects.create(work_site=work_site, user=user, role=role)

        response_data = UserSerializer(user, context={'request':request}).data
        return Response(response_data)


class GetWorkSites(ListAPIView):
    permission_classes = [IsAuthenticated, IsEPCAdmin]
    serializer_class = WorkSiteSerializer
    queryset = WorkSite.objects.all()

