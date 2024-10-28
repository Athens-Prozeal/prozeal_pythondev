from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date

from authentication.permissions import HasWorkSitePermission
from safety_observation.permissions import SafetyObservationPermission , ObservationClassificationPermission, CorrectiveActionPermission, ReviewCorrectiveActionPermission
from safety_observation.models import SafetyObservation, ObservationClassification
from .serializers import SafetyObservationSerializer

class GetObservationClassification(ListAPIView):
    class ObservationSerializer(ModelSerializer):
        class Meta:
            model = ObservationClassification
            fields = ('name', )

    permission_classes = [IsAuthenticated, HasWorkSitePermission, ObservationClassificationPermission]
    serializer_class = ObservationSerializer
    queryset = ObservationClassification.objects.all()


class SafetyObservationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, SafetyObservationPermission]
    serializer_class = SafetyObservationSerializer

    def get_queryset(self):
        work_site = self.request.work_site
        return SafetyObservation.objects.filter(work_site=work_site)

    def list(self, request, *args, **kwargs):
        work_site = self.request.work_site
        user = self.request.user
        observation_status = self.request.query_params.get("status")
        safety_observations = SafetyObservation.objects.filter(work_site=work_site)

        if observation_status == "open":
            safety_observations = safety_observations.filter(observation_status="open")
        elif observation_status == "closed":
            safety_observations = safety_observations.filter(observation_status="closed")
        elif observation_status == "corrective-action-required":
            safety_observations = safety_observations.filter(status="open").filter(
                corrective_action_assigned_to=user
            )
        elif observation_status == "verification-required":
            safety_observations = safety_observations.filter(status="verification_required").filter(
                reported_by=user
            )

        serializer = self.get_serializer(safety_observations, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        work_site = self.request.work_site
        user = self.request.user
        data = serializer.validated_data

        if data["observation_status"] == "open":
            data["closed_on"] = None
            data["after_image"] = None
            data["status"] = "open"

        elif data["observation_status"] == "closed":
            data["closed_on"] = date.today()
            data["status"] = "closed"

        serializer.save(
            work_site=work_site,
            reported_by=user,
            created_by=user,
            last_updated_by=user,
        )

    def perform_destroy(self, instance):
        instance.delete()


class SubmitCorrectiveAction(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, CorrectiveActionPermission,]

    def put(self, request, pk):
        user = request.user
        safety_observation = SafetyObservation.objects.get(id=pk)

        if user != safety_observation.corrective_action_assigned_to:
            return Response({"message": "Not allowed"}, status=403)
        
        if safety_observation.status == 'verification_required':
            return Response({"message": "Verification is pending"}, status=403)

        safety_observation.corrective_action_taken =  request.data["corrective_action_taken"]
        safety_observation.after_image = request.data["after_image"]
        safety_observation.status = "verification_required"
        safety_observation.save()

        return Response({"message": "Corrective action submitted successfully"})


class VerifyCorrectiveAction(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, ReviewCorrectiveActionPermission]

    def put(self, request, pk):
        user = request.user
        safety_observation = SafetyObservation.objects.get(id=pk)

        if user != safety_observation.reported_by:
            return Response({"message": "Not allowed"}, status=403)
        
        if safety_observation.status != 'verification_required':
            return Response({"message": "No corrective action to verify"}, status=403)
        
        safety_observation.status = "closed"
        safety_observation.observation_status = "closed"
        safety_observation.closed_on = date.today()
        safety_observation.save()

        return Response({"message": "Corrective action verified successfully"})


class RejectCorrectiveAction(APIView):
    permission_classes = [IsAuthenticated, HasWorkSitePermission, ReviewCorrectiveActionPermission]
    
    def put(self, request, pk):
        user = request.user
        safety_observation = SafetyObservation.objects.get(id=pk)

        if user != safety_observation.reported_by:
            return Response({"message": "Not allowed"}, status=403)
        
        if safety_observation.status != 'verification_required':
            return Response({"message": "No corrective action to verify"}, status=403)
        
        safety_observation.status = "open"
        safety_observation.after_image = None
        safety_observation.corrective_action_taken = None
        safety_observation.save()

        return Response({"message": "Corrective action rejected successfully"})

