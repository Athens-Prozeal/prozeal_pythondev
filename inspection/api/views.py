from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import HasWorkSitePermission, is_epc_admin
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from datetime import datetime

from inspection.permissions import InspectionPermission, InspectionApprovePermission
from .serializers import (
    ExcavationSerializer, AntiTermiteTreatmentSerializer, PlainCementConcreteWorkSerializer, PourCardForColumnConcreteSerializer, PourCardForSlabConcreteSerializer, PourCardForBeamSerializer, PlasteringSerializer,
    HTCableSerializer, CCTVInstallationSerializer, CulvertWorkSerializer, RemoteTerminalUnitSerializer, UPSSerializer, ICOGPanelSerializer, PaintingSerializer, RCCSerializer, ACDistributionBoardSerializer, AUXTransformerSerializer, BusductSerializer, HighVoltagePanelSerializer, PeripheryLightingSerializer, PlumbingSerializer, ScadaSystemSerializer, WMSSerializer, PlantBoundaryAndFencingSerializer, ChainLinkFencingSerializer, PotentialTransformerSerializer, BatteryBankAndBatteryChargerSerializer, ControlCableLayingSerializer, FireAlarmPanelSerializer, InverterSerializer, StringCablesSerializer, LightningArresterSerializer, StringCables2Serializer, NIFPSSerializer, 
    DCDBSerializer, ModuleInterconnectionSerializer, OutdoorIsolatorOrEarthSwitchSerializer, TransmissionLinesSerializer, InverterOrControlRoomBuildingSerializer,
    InverterDutyTransformerSerializer, SPVModulesSerializer,
    EarthingSystemSerializer, HTCablePreComSerializer,
)

from inspection.models import (
    Excavation, AntiTermiteTreatment, PourCardForColumnConcrete, PourCardForSlabConcrete, PourCardForBeam, PlainCementConcreteWork, Plastering,
    HTCable, CCTVInstallation, CulvertWork, RemoteTerminalUnit, UPS, ICOGPanel, Painting, RCC, ACDistributionBoard, AUXTransformer, Busduct, HighVoltagePanel, PeripheryLighting, Plumbing, ScadaSystem, WMS, PlantBoundaryAndFencing, ChainLinkFencing, PotentialTransformer, BatteryBankAndBatteryCharger, ControlCableLaying, FireAlarmPanel, Inverter, StringCables, LightningArrester, StringCables2, NIFPS,
    DCDB, ModuleInterconnection, OutdoorIsolatorOrEarthSwitch, TransmissionLines, InverterOrControlRoomBuilding,
    InverterDutyTransformer, SPVModules, 
    EarthingSystem, HTCablePreCom,
)

class Inspection3WBaseViewSet(viewsets.ModelViewSet):
    """ Update not allowed """
    permission_classes = [IsAuthenticated, HasWorkSitePermission, InspectionPermission]

    def get_queryset(self):
        work_site = self.request.work_site
        return self.model.objects.filter(work_site=work_site)
    
    def list(self, request, *args, **kwargs): 
        work_site = self.request.work_site
        user = self.request.user
        approval_status = self.request.query_params.get('status')
        inspections = self.model.objects.filter(work_site=work_site)

        if approval_status == 'action-required':
                inspections = inspections.filter(Q(approval_status='in_progress') | Q(approval_status='initiated'))

                inspections = inspections.filter(
                    Q(witness_1=user, witness_1_approved=False) |
                    Q(witness_2=user, witness_2_approved=False) |
                    Q(witness_3=user, witness_3_approved=False)
                )   

        elif approval_status == 'initiated':
            if is_epc_admin(user):
                inspections = inspections.filter(approval_status='initiated')
            else:
                inspections = inspections.filter(approval_status='initiated').filter(Q(checked_by=user) | Q(witness_1=user) | Q(witness_2=user) | Q(witness_3=user))
    
        elif approval_status == 'in-progress':
            if is_epc_admin(user):
                inspections = inspections.filter(approval_status='in_progress')
            else:
                inspections = inspections.filter(approval_status='in_progress').filter(Q(checked_by=user) | Q(witness_1=user) | Q(witness_2=user) | Q(witness_3=user))

        else:
            inspections = inspections.filter(approval_status='approved')

        serializer = self.get_serializer(inspections, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        work_site = self.request.work_site
        serializer.save(
            checked_by = self.request.user,
            work_site = work_site,
            created_by=self.request.user,
            last_updated_by=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.delete()


class ApproveInspection3WBaseView(APIView): # Base class for approving inspections
    permission_classes = [IsAuthenticated, HasWorkSitePermission, InspectionApprovePermission] # Not callable

    def put(self, request, pk, *args, **kwargs):
        inspection = get_object_or_404(self.model, id=pk)
        user = request.user
        signature = request.data.get('signature')
        
        if user == inspection.witness_1 and not inspection.witness_1_approved:
            inspection.witness_1_approved = True
            inspection.witness_1_signature = signature
            inspection.witness_1_date = datetime.date(datetime.now())
        
        elif user == inspection.witness_2 and not inspection.witness_2_approved:
            inspection.witness_2_approved = True
            inspection.witness_2_signature = signature
            inspection.witness_2_date = datetime.date(datetime.now())
        
        elif user == inspection.witness_3 and not inspection.witness_3_approved:
            inspection.witness_3_approved = True
            inspection.witness_3_signature = signature
            inspection.witness_3_date = datetime.date(datetime.now())

        else:
            return Response({'message': 'Not allowed'}, status=400)

        inspection.last_updated_by = user
        inspection.save()

        # Update the status of the inspection
        if inspection.witness_1_approved or inspection.witness_2_approved or inspection.witness_3_approved:
            if inspection.witness_1_approved and inspection.witness_2_approved and inspection.witness_3_approved:
                inspection.approval_status = 'approved'       
            else:
                inspection.approval_status = 'in_progress'
            
            inspection.save()

        return Response({'message': 'Inspection approved successfully'}, status=200)
    

# 2 witness
class Inspection2WBaseViewSet(viewsets.ModelViewSet):
    """ Update not allowed """
    permission_classes = [IsAuthenticated, HasWorkSitePermission, InspectionPermission]

    def get_queryset(self):
        work_site = self.request.work_site
        return self.model.objects.filter(work_site=work_site)
    
    def list(self, request, *args, **kwargs): 
        work_site = self.request.work_site
        user = self.request.user
        approval_status = self.request.query_params.get('status')
        inspections = self.model.objects.filter(work_site=work_site)

        if approval_status == 'action-required':
                inspections = inspections.filter(Q(approval_status='in_progress') | Q(approval_status='initiated'))

                inspections = inspections.filter(
                    Q(witness_1=user, witness_1_approved=False) |
                    Q(witness_2=user, witness_2_approved=False)
                )   

        elif approval_status == 'initiated':
            if is_epc_admin(user):
                inspections = inspections.filter(approval_status='initiated')
            else:
                inspections = inspections.filter(approval_status='initiated').filter(Q(checked_by=user) | Q(witness_1=user) | Q(witness_2=user))
    
        elif approval_status == 'in-progress':
            if is_epc_admin(user):
                inspections = inspections.filter(approval_status='in_progress')
            else:
                inspections = inspections.filter(approval_status='in_progress').filter(Q(checked_by=user) | Q(witness_1=user) | Q(witness_2=user))

        else:
            inspections = inspections.filter(approval_status='approved')

        serializer = self.get_serializer(inspections, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        work_site = self.request.work_site
        serializer.save(
            checked_by = self.request.user,
            work_site = work_site,
            created_by=self.request.user,
            last_updated_by=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.delete()


class ApproveInspection2WBaseView(APIView): # Base class for approving inspections
    permission_classes = [IsAuthenticated, HasWorkSitePermission, InspectionApprovePermission] # Not callable

    def put(self, request, pk, *args, **kwargs):
        inspection = get_object_or_404(self.model, id=pk)
        user = request.user
        signature = request.data.get('signature')
        
        if user == inspection.witness_1 and not inspection.witness_1_approved:
            inspection.witness_1_approved = True
            inspection.witness_1_signature = signature
            inspection.witness_1_date = datetime.date(datetime.now())
        
        elif user == inspection.witness_2 and not inspection.witness_2_approved:
            inspection.witness_2_approved = True
            inspection.witness_2_signature = signature
            inspection.witness_2_date = datetime.date(datetime.now())

        else:
            return Response({'message': 'Not allowed'}, status=400)
        
        inspection.last_updated_by = user
        inspection.save()

        # Update the status of the inspection
        if inspection.witness_1_approved or inspection.witness_2_approved:
            if inspection.witness_1_approved and inspection.witness_2_approved:
                inspection.approval_status = 'approved'       
            else:
                inspection.approval_status = 'in_progress'
            
            inspection.save()

        return Response({'message': 'Inspection approved successfully'}, status=200)
    


# Categorized checklists 
class ExcavationViewSet(Inspection3WBaseViewSet):
    model = Excavation
    serializer_class = ExcavationSerializer
 
class ApproveExcavation(ApproveInspection3WBaseView):
    model = Excavation


class AntiTermiteTreatmentViewSet(Inspection3WBaseViewSet):
    model = AntiTermiteTreatment
    serializer_class = AntiTermiteTreatmentSerializer

class ApproveAntiTermiteTreatment(ApproveInspection3WBaseView):
    model = AntiTermiteTreatment


class PlainCementConcreteWorkViewSet(Inspection3WBaseViewSet):
    model = PlainCementConcreteWork
    serializer_class = PlainCementConcreteWorkSerializer

class ApprovePlainCementConcreteWork(ApproveInspection3WBaseView):
    model = PlainCementConcreteWork


# POUR CARDS
class PourCardForColumnConcreteViewSet(Inspection3WBaseViewSet):
    model = PourCardForColumnConcrete
    serializer_class = PourCardForColumnConcreteSerializer

class ApprovePourCardForColumnConcrete(ApproveInspection3WBaseView):
    model = PourCardForColumnConcrete


class PourCardForSlabConcreteViewSet(Inspection3WBaseViewSet):
    model = PourCardForSlabConcrete
    serializer_class = PourCardForSlabConcreteSerializer

class ApprovePourCardForSlabConcrete(ApproveInspection3WBaseView):
    model = PourCardForSlabConcrete


class PourCardForBeamViewSet(Inspection3WBaseViewSet):
    model = PourCardForBeam
    serializer_class = PourCardForBeamSerializer

class ApprovePourCardForBeam(ApproveInspection3WBaseView):
    model = PourCardForBeam


class PlasteringViewSet(Inspection3WBaseViewSet):
    model = Plastering
    serializer_class = PlasteringSerializer

class ApprovePlastering(ApproveInspection3WBaseView):
    model = Plastering


# UN Categorized checklists 
class HTCableViewSet(Inspection3WBaseViewSet):
    model = HTCable
    serializer_class = HTCableSerializer

class ApproveHTCable(ApproveInspection3WBaseView):
    model = HTCable


class CCTVInstallationViewSet(Inspection3WBaseViewSet):
    model = CCTVInstallation
    serializer_class = CCTVInstallationSerializer

class ApproveCCTVInstallation(ApproveInspection3WBaseView):
    model = CCTVInstallation


class CulvertWorkViewSet(Inspection3WBaseViewSet):
    model = CulvertWork
    serializer_class = CulvertWorkSerializer

class ApproveCulvertWork(ApproveInspection3WBaseView):
    model = CulvertWork


class RemoteTerminalUnitViewSet(Inspection3WBaseViewSet):
    model = RemoteTerminalUnit
    serializer_class = RemoteTerminalUnitSerializer

class ApproveRemoteTerminalUnit(ApproveInspection3WBaseView):
    model = RemoteTerminalUnit


class UPSViewSet(Inspection3WBaseViewSet):
    model = UPS
    serializer_class = UPSSerializer

class ApproveUPS(ApproveInspection3WBaseView):
    model = UPS


class ICOGPanelViewSet(Inspection3WBaseViewSet):
    model = ICOGPanel
    serializer_class = ICOGPanelSerializer

class ApproveICOGPanel(ApproveInspection3WBaseView):
    model = ICOGPanel


class PaintingViewSet(Inspection3WBaseViewSet):
    model = Painting
    serializer_class = PaintingSerializer

class ApprovePainting(ApproveInspection3WBaseView):
    model = Painting


class RCCViewSet(Inspection3WBaseViewSet):
    model = RCC
    serializer_class = RCCSerializer

class ApproveRCC(ApproveInspection3WBaseView):
    model = RCC


class ACDistributionBoardViewSet(Inspection3WBaseViewSet):
    model = ACDistributionBoard
    serializer_class = ACDistributionBoardSerializer

class ApproveACDistributionBoard(ApproveInspection3WBaseView):
    model = ACDistributionBoard


class AUXTransformerViewSet(Inspection3WBaseViewSet):
    model = AUXTransformer
    serializer_class = AUXTransformerSerializer

class ApproveAUXTransformer(ApproveInspection3WBaseView):
    model = AUXTransformer


class BusductViewSet(Inspection3WBaseViewSet):
    model = Busduct
    serializer_class = BusductSerializer

class ApproveBusduct(ApproveInspection3WBaseView):
    model = Busduct


class HighVoltagePanelViewSet(Inspection3WBaseViewSet):
    model = HighVoltagePanel
    serializer_class = HighVoltagePanelSerializer

class ApproveHighVoltagePanel(ApproveInspection3WBaseView):
    model = HighVoltagePanel


class PeripheryLightingViewSet(Inspection3WBaseViewSet):
    model = PeripheryLighting
    serializer_class = PeripheryLightingSerializer

class ApprovePeripheryLighting(ApproveInspection3WBaseView):
    model = PeripheryLighting


class PlumbingViewSet(Inspection3WBaseViewSet):
    model = Plumbing
    serializer_class = PlumbingSerializer

class ApprovePlumbing(ApproveInspection3WBaseView):
    model = Plumbing


class ScadaSystemViewSet(Inspection3WBaseViewSet):
    model = ScadaSystem
    serializer_class = ScadaSystemSerializer

class ApproveScadaSystem(ApproveInspection3WBaseView):
    model = ScadaSystem


class WMSViewSet(Inspection3WBaseViewSet):
    model = WMS
    serializer_class = WMSSerializer

class ApproveWMS(ApproveInspection3WBaseView):
    model = WMS


class PlantBoundaryAndFencingViewSet(Inspection3WBaseViewSet):
    model = PlantBoundaryAndFencing
    serializer_class = PlantBoundaryAndFencingSerializer

class ApprovePlantBoundaryAndFencing(ApproveInspection3WBaseView):
    model = PlantBoundaryAndFencing


class ChainLinkFencingViewSet(Inspection3WBaseViewSet):
    model = ChainLinkFencing
    serializer_class = ChainLinkFencingSerializer

class ApproveChainLinkFencing(ApproveInspection3WBaseView):
    model = ChainLinkFencing


class PotentialTransformerViewSet(Inspection3WBaseViewSet):
    model = PotentialTransformer
    serializer_class = PotentialTransformerSerializer

class ApprovePotentialTransformer(ApproveInspection3WBaseView):
    model = PotentialTransformer


class BatteryBankAndBatteryChargerViewSet(Inspection3WBaseViewSet):
    model = BatteryBankAndBatteryCharger
    serializer_class = BatteryBankAndBatteryChargerSerializer

class ApproveBatteryBankAndBatteryCharger(ApproveInspection3WBaseView):
    model = BatteryBankAndBatteryCharger


class ControlCableLayingViewSet(Inspection3WBaseViewSet):
    model = ControlCableLaying
    serializer_class = ControlCableLayingSerializer

class ApproveControlCableLaying(ApproveInspection3WBaseView):
    model = ControlCableLaying


class FireAlarmPanelViewSet(Inspection3WBaseViewSet):
    model = FireAlarmPanel
    serializer_class = FireAlarmPanelSerializer

class ApproveFireAlarmPanel(ApproveInspection3WBaseView):
    model = FireAlarmPanel


class InverterViewSet(Inspection3WBaseViewSet):
    model = Inverter
    serializer_class = InverterSerializer

class ApproveInverter(ApproveInspection3WBaseView):
    model = Inverter


class StringCablesViewSet(Inspection3WBaseViewSet):
    model = StringCables
    serializer_class = StringCablesSerializer

class ApproveStringCables(ApproveInspection3WBaseView):
    model = StringCables


class LightningArresterViewSet(Inspection3WBaseViewSet):
    model = LightningArrester
    serializer_class = LightningArresterSerializer

class ApproveLightningArrester(ApproveInspection3WBaseView):
    model = LightningArrester


class StringCables2ViewSet(Inspection3WBaseViewSet):
    model = StringCables2
    serializer_class = StringCables2Serializer

class ApproveStringCables2(ApproveInspection3WBaseView):
    model = StringCables2


class NIFPSViewSet(Inspection3WBaseViewSet):
    model = NIFPS
    serializer_class = NIFPSSerializer

class ApproveNIFPS(ApproveInspection3WBaseView):
    model = NIFPS


# 2 witness
class DCDBViewSet(Inspection2WBaseViewSet):
    model = DCDB
    serializer_class = DCDBSerializer

class ApproveDCDB(ApproveInspection2WBaseView):
    model = DCDB


class ModuleInterconnectionViewSet(Inspection2WBaseViewSet):
    model = ModuleInterconnection
    serializer_class = ModuleInterconnectionSerializer

class ApproveModuleInterconnection(ApproveInspection2WBaseView):
    model = ModuleInterconnection


class OutdoorIsolatorOrEarthSwitchViewSet(Inspection2WBaseViewSet):
    model = OutdoorIsolatorOrEarthSwitch
    serializer_class = OutdoorIsolatorOrEarthSwitchSerializer

class ApproveOutdoorIsolatorOrEarthSwitch(ApproveInspection2WBaseView):
    model = OutdoorIsolatorOrEarthSwitch


class TransmissionLinesViewSet(Inspection2WBaseViewSet):
    model = TransmissionLines
    serializer_class = TransmissionLinesSerializer

class ApproveTransmissionLines(ApproveInspection2WBaseView):
    model = TransmissionLines


class InverterOrControlRoomBuildingViewSet(Inspection2WBaseViewSet):
    model = InverterOrControlRoomBuilding
    serializer_class = InverterOrControlRoomBuildingSerializer

class ApproveInverterOrControlRoomBuilding(ApproveInspection2WBaseView):
    model = InverterOrControlRoomBuilding


class InverterDutyTransformerViewSet(Inspection3WBaseViewSet):
    model = InverterDutyTransformer
    serializer_class = InverterDutyTransformerSerializer

class ApproveInverterDutyTransformer(ApproveInspection3WBaseView):
    model = InverterDutyTransformer


class SPVModulesViewSet(Inspection2WBaseViewSet):
    model = SPVModules
    serializer_class = SPVModulesSerializer

class ApproveSPVModules(ApproveInspection2WBaseView):
    model = SPVModules


class EarthingSystemViewSet(Inspection3WBaseViewSet):
    model = EarthingSystem
    serializer_class = EarthingSystemSerializer

class ApproveEarthingSystem(ApproveInspection3WBaseView):
    model = EarthingSystem


class HTCablePreComViewSet(Inspection3WBaseViewSet):
    model = HTCablePreCom
    serializer_class = HTCablePreComSerializer

class ApproveHTCablePreCom(ApproveInspection3WBaseView):
    model = HTCablePreCom

