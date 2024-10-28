from rest_framework.serializers import ModelSerializer, CharField

from inspection.models import (
    Excavation, AntiTermiteTreatment, PourCardForColumnConcrete, PourCardForSlabConcrete, PourCardForBeam, PlainCementConcreteWork, Plastering,
    HTCable, CCTVInstallation, CulvertWork, RemoteTerminalUnit, UPS, ICOGPanel, Painting, RCC, ACDistributionBoard, AUXTransformer, Busduct, HighVoltagePanel, PeripheryLighting, Plumbing, ScadaSystem, WMS, PlantBoundaryAndFencing, ChainLinkFencing, PotentialTransformer, BatteryBankAndBatteryCharger, ControlCableLaying, FireAlarmPanel, Inverter, StringCables, LightningArrester, StringCables2, NIFPS,
    DCDB, ModuleInterconnection, OutdoorIsolatorOrEarthSwitch, TransmissionLines, InverterOrControlRoomBuilding,
    InverterDutyTransformer, SPVModules, 
    EarthingSystem, HTCablePreCom,
)
from inspection.permissions import check_obj_permission 


class Inspection3WBaseSerializer(ModelSerializer):
    checked_by_username = CharField(source='checked_by.username', required=False, read_only=True)
    witness_1_full_name = CharField(source='witness_1.full_name', required=False, read_only=True)
    witness_2_full_name = CharField(source='witness_2.full_name', required=False, read_only=True)
    witness_3_full_name = CharField(source='witness_3.full_name', required=False, read_only=True)
    witness_1_company = CharField(source='witness_1.company', required=False, read_only=True)
    witness_2_company = CharField(source='witness_2.company', required=False, read_only=True)
    witness_3_company = CharField(source='witness_3.company', required=False, read_only=True)
    read_only_fields = ('approval_status', 'checked_by_date', 'witness_1_approved', 'witness_2_approved', 'witness_3_approved', 'witness_1_date', 'witness_2_date', 'witness_3_date', 'witness_1_signature', 'witness_2_signature', 'witness_3_signature') 
    exclude = ('checked_by', 'work_site', 'created_by', 'last_updated_by', 'created_at', 'last_updated_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        work_site = self.context['request'].work_site
        work_site_id = work_site.id
        
        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "approve": {
                "name": "approve",
                "method": "PUT",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/approve/?work_site_id={work_site_id}",
            },
        }

        allowed_actions = []
        
        if check_obj_permission(user, work_site, 'retrieve', instance):
            allowed_actions.append(actions["view"])

        if check_obj_permission(user, work_site, 'destroy', instance):
            allowed_actions.append(actions["delete"])
            
        # Approve action
        if instance.witness_1 == user and not instance.witness_1_approved:
            allowed_actions.append(actions["approve"])

        if instance.witness_2 == user and not instance.witness_2_approved:
            allowed_actions.append(actions["approve"])

        if instance.witness_3 == user and not instance.witness_3_approved:
            allowed_actions.append(actions["approve"])

        data["actions"] = allowed_actions

        return data
    

class Inspection2WBaseSerializer(ModelSerializer):
    checked_by_username = CharField(source='checked_by.username', required=False, read_only=True)
    witness_1_full_name = CharField(source='witness_1.full_name', required=False, read_only=True)
    witness_2_full_name = CharField(source='witness_2.full_name', required=False, read_only=True)
    witness_1_company = CharField(source='witness_1.company', required=False, read_only=True)
    witness_2_company = CharField(source='witness_2.company', required=False, read_only=True)
    read_only_fields = ('approval_status', 'checked_by_date', 'witness_1_approved', 'witness_2_approved',  'witness_1_date', 'witness_2_date', 'witness_1_signature', 'witness_2_signature') 
    exclude = ('checked_by', 'work_site', 'created_by', 'last_updated_by', 'created_at', 'last_updated_at',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        work_site = self.context['request'].work_site
        work_site_id = work_site.id
        
        actions = {
            "view": {
                "name": "view",
                "method": "GET",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "delete": {
                "name": "delete",
                "method": "DELETE",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/?work_site_id={work_site_id}",
            },
            "approve": {
                "name": "approve",
                "method": "PUT",
                "url": f"/api/inspection/{instance.table_identifier}/{instance.id}/approve/?work_site_id={work_site_id}",
            },
        }

        allowed_actions = []
        
        if check_obj_permission(user, work_site, 'retrieve', instance):
            allowed_actions.append(actions["view"])

        if check_obj_permission(user, work_site, 'destroy', instance):
            allowed_actions.append(actions["delete"])
            
        # Approve action
        if instance.witness_1 == user and not instance.witness_1_approved:
            allowed_actions.append(actions["approve"])

        if instance.witness_2 == user and not instance.witness_2_approved:
            allowed_actions.append(actions["approve"])

        data["actions"] = allowed_actions

        return data
    

# 3 witness
# Category checklists
class ExcavationSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Excavation
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude 


class AntiTermiteTreatmentSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = AntiTermiteTreatment
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


# Pour Card
class PourCardForColumnConcreteSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PourCardForColumnConcrete
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PourCardForSlabConcreteSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PourCardForSlabConcrete
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PourCardForBeamSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PourCardForBeam
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude

class PlainCementConcreteWorkSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PlainCementConcreteWork
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude

class PlasteringSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Plastering
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


# No category checklists
class HTCableSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = HTCable
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class CCTVInstallationSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = CCTVInstallation
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class CulvertWorkSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = CulvertWork
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class RemoteTerminalUnitSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = RemoteTerminalUnit
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class UPSSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = UPS
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class ICOGPanelSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = ICOGPanel
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PaintingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Painting
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class RCCSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = RCC
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class ACDistributionBoardSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = ACDistributionBoard
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class AUXTransformerSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = AUXTransformer
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class BusductSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Busduct
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class HighVoltagePanelSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = HighVoltagePanel
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PeripheryLightingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PeripheryLighting
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PlumbingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Plumbing
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class ScadaSystemSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = ScadaSystem
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class WMSSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = WMS
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class PlantBoundaryAndFencingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PlantBoundaryAndFencing
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class ChainLinkFencingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = ChainLinkFencing
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude
      

class PotentialTransformerSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = PotentialTransformer
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class BatteryBankAndBatteryChargerSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = BatteryBankAndBatteryCharger
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class ControlCableLayingSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = ControlCableLaying
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class FireAlarmPanelSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = FireAlarmPanel
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class InverterSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = Inverter
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class StringCablesSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = StringCables
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class LightningArresterSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = LightningArrester
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class StringCables2Serializer(Inspection3WBaseSerializer):
    class Meta:
        model = StringCables2
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class NIFPSSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = NIFPS
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


# 2 Witness
class DCDBSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = DCDB
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class ModuleInterconnectionSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = ModuleInterconnection
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class OutdoorIsolatorOrEarthSwitchSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = OutdoorIsolatorOrEarthSwitch
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class TransmissionLinesSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = TransmissionLines
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class InverterOrControlRoomBuildingSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = InverterOrControlRoomBuilding
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class InverterDutyTransformerSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = InverterDutyTransformer
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class SPVModulesSerializer(Inspection2WBaseSerializer):
    class Meta:
        model = SPVModules
        read_only_fields = Inspection2WBaseSerializer.read_only_fields
        exclude = Inspection2WBaseSerializer.exclude


class EarthingSystemSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = EarthingSystem
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude


class HTCablePreComSerializer(Inspection3WBaseSerializer):
    class Meta:
        model = HTCablePreCom
        read_only_fields = Inspection3WBaseSerializer.read_only_fields
        exclude = Inspection3WBaseSerializer.exclude

