from django.urls import path
from rest_framework import routers

from .views import( 
    # Categorized checklists
    ExcavationViewSet, AntiTermiteTreatmentViewSet, PlainCementConcreteWorkViewSet, PourCardForColumnConcreteViewSet, PourCardForSlabConcreteViewSet, PourCardForBeamViewSet, PlasteringViewSet,
    ApproveExcavation, ApproveAntiTermiteTreatment, ApprovePlainCementConcreteWork, ApprovePourCardForColumnConcrete, ApprovePourCardForSlabConcrete, ApprovePourCardForBeam, ApprovePlastering,

    # Un Categorized checklists
    HTCableViewSet, CCTVInstallationViewSet, CulvertWorkViewSet, NIFPSViewSet, RemoteTerminalUnitViewSet, UPSViewSet, ICOGPanelViewSet, PaintingViewSet, RCCViewSet, ACDistributionBoardViewSet, AUXTransformerViewSet, BusductViewSet, HighVoltagePanelViewSet, PeripheryLightingViewSet, PlumbingViewSet, ScadaSystemViewSet, WMSViewSet, PlantBoundaryAndFencingViewSet, ChainLinkFencingViewSet, PotentialTransformerViewSet, BatteryBankAndBatteryChargerViewSet, ControlCableLayingViewSet, FireAlarmPanelViewSet, InverterViewSet, StringCablesViewSet, LightningArresterViewSet, StringCables2ViewSet, 
    ApproveHTCable, ApproveCCTVInstallation, ApproveCulvertWork, ApproveNIFPS, ApproveRemoteTerminalUnit, ApproveUPS, ApproveICOGPanel, ApprovePainting, ApproveRCC, ApproveACDistributionBoard, ApproveAUXTransformer, ApproveBusduct, ApproveHighVoltagePanel, ApprovePeripheryLighting, ApprovePlumbing, ApproveScadaSystem, ApproveWMS, ApprovePlantBoundaryAndFencing, ApproveChainLinkFencing, ApprovePotentialTransformer, ApproveBatteryBankAndBatteryCharger, ApproveControlCableLaying, ApproveFireAlarmPanel, ApproveInverter, ApproveStringCables, ApproveLightningArrester, ApproveStringCables2,

    # 2 witness
    DCDBViewSet, OutdoorIsolatorOrEarthSwitchViewSet, TransmissionLinesViewSet, InverterOrControlRoomBuildingViewSet,
    ApproveDCDB, ApproveOutdoorIsolatorOrEarthSwitch, ApproveTransmissionLines, ApproveInverterOrControlRoomBuilding,

    # Complex checklists
    InverterDutyTransformerViewSet, SPVModulesViewSet,
    ApproveInverterDutyTransformer, ApproveSPVModules,

    # Complex forms
    EarthingSystemViewSet, HTCablePreComViewSet,
    ApproveEarthingSystem, ApproveHTCablePreCom
) 

router = routers.SimpleRouter()

# Categorized checklists
router.register('excavation', ExcavationViewSet, basename='excavation')
router.register('anti-termite-treatment', AntiTermiteTreatmentViewSet, basename='anti-termite-treatment')
router.register('plain-cement-concrete-work', PlainCementConcreteWorkViewSet, basename='plain-cement-concrete-work')
router.register('pour-card-for-column-concrete', PourCardForColumnConcreteViewSet, basename='pour-card-for-column-concrete')
router.register('pour-card-for-slab-concrete', PourCardForSlabConcreteViewSet, basename='pour-card-for-slab-concrete')
router.register('pour-card-for-beam', PourCardForBeamViewSet, basename='pour-card-for-beam')
router.register('plastering', PlasteringViewSet, basename='plastering')

# Un Categorized checklists
router.register('ht-cable', HTCableViewSet, basename='ht-cable')
router.register('cctv-installation', CCTVInstallationViewSet, basename='cctv-installation')
router.register('culvert-work', CulvertWorkViewSet, basename='culvert-work')
router.register('nifps', NIFPSViewSet, basename='nifps')
router.register('remote-terminal-unit', RemoteTerminalUnitViewSet, basename='remote-terminal-unit')
router.register('ups', UPSViewSet, basename='ups')
router.register('icog-panel', ICOGPanelViewSet, basename='icog-panel')
router.register('painting', PaintingViewSet, basename='painting')
router.register('rcc', RCCViewSet, basename='rcc')
router.register('ac-distribution-board', ACDistributionBoardViewSet, basename='ac-distribution-board')
router.register('aux-transformer', AUXTransformerViewSet, basename='aux-transformer')
router.register('busduct', BusductViewSet, basename='busduct')
router.register('high-voltage-panel', HighVoltagePanelViewSet, basename='high-voltage-panel')
router.register('periphery-lighting', PeripheryLightingViewSet, basename='periphery-lighting')
router.register('plumbing', PlumbingViewSet, basename='plumbing')
router.register('scada-system', ScadaSystemViewSet, basename='scada-system')
router.register('wms', WMSViewSet, basename='wms')
router.register('plant-boundary-and-fencing', PlantBoundaryAndFencingViewSet, basename='plant-boundary-and-fencing')
router.register('chain-link-fencing', ChainLinkFencingViewSet, basename='chain-link-fencing')
router.register('potential-transformer', PotentialTransformerViewSet, basename='potential-transformer')
router.register('battery-bank-and-battery-charger', BatteryBankAndBatteryChargerViewSet, basename='battery-bank-and-battery-charger')
router.register('control-cable-laying', ControlCableLayingViewSet, basename='control-cable-laying')
router.register('fire-alarm-panel', FireAlarmPanelViewSet, basename='fire-alarm-panel')
router.register('inverter', InverterViewSet, basename='inverter')
router.register('string-cables', StringCablesViewSet, basename='string-cables')
router.register('lightning-arrester', LightningArresterViewSet, basename='lightning-arrester')
router.register('string-cables2', StringCables2ViewSet, basename='string-cables2')

# 2 witness
router.register('dcdb', DCDBViewSet, basename='dcdb')
router.register('outdoor-isolator-or-earth-switch', OutdoorIsolatorOrEarthSwitchViewSet, basename='outdoor-isolator-or-earth-switch')
router.register('transmission-lines', TransmissionLinesViewSet, basename='transmission-lines')
router.register('inverter-or-control-room-building', InverterOrControlRoomBuildingViewSet, basename='inverter-room-or-control-room')

# Complex checklists
router.register('inverter-duty-transformer', InverterDutyTransformerViewSet, basename='inverter-duty-transformer')
router.register('spv-modules', SPVModulesViewSet, basename='spv-modules')

# Complex forms
router.register('earthing-system', EarthingSystemViewSet, basename='earthing-system')
router.register('ht-cable-pre-com', HTCablePreComViewSet, basename='ht-cable-pre-com')


urlpatterns = [
    # Categorized checklists
    path('excavation/<uuid:pk>/approve/', ApproveExcavation.as_view(), name='approve_excavation_inspection'),
    path('anti-termite-treatment/<uuid:pk>/approve/', ApproveAntiTermiteTreatment.as_view(), name='approve_anti_termite_treatment_inspection'),
    path('plain-cement-concrete-work/<uuid:pk>/approve/', ApprovePlainCementConcreteWork.as_view(), name='approve_plain_cement_concrete_work_inspection'),
    path('pour-card-for-column-concrete/<uuid:pk>/approve/', ApprovePourCardForColumnConcrete.as_view(), name='approve_pour_card_for_column_concrete_inspection'),
    path('pour-card-for-slab-concrete/<uuid:pk>/approve/', ApprovePourCardForSlabConcrete.as_view(), name='approve_pour_card_for_slab_concrete_inspection'),
    path('pour-card-for-beam/<uuid:pk>/approve/', ApprovePourCardForBeam.as_view(), name='approve_pour_card_for_beam_inspection'),
    path('plastering/<uuid:pk>/approve/', ApprovePlastering.as_view(), name='approve_plastering_inspection'),

    # Un Categorized checklists
    path('ht-cable/<uuid:pk>/approve/', ApproveHTCable.as_view(), name='approve_ht_cable_inspection'),
    path('cctv-installation/<uuid:pk>/approve/', ApproveCCTVInstallation.as_view(), name='approve_cctv_installation_inspection'),
    path('culvert-work/<uuid:pk>/approve/', ApproveCulvertWork.as_view(), name='approve_culvert_work_inspection'),
    path('nifps/<uuid:pk>/approve/', ApproveNIFPS.as_view(), name='approve_nifps_inspection'),
    path('remote-terminal-unit/<uuid:pk>/approve/', ApproveRemoteTerminalUnit.as_view(), name='approve_remote_terminal_unit_inspection'),
    path('ups/<uuid:pk>/approve/', ApproveUPS.as_view(), name='approve_ups_inspection'),
    path('icog-panel/<uuid:pk>/approve/', ApproveICOGPanel.as_view(), name='approve_icog_panel_inspection'),
    path('painting/<uuid:pk>/approve/', ApprovePainting.as_view(), name='approve_painting_inspection'),
    path('rcc/<uuid:pk>/approve/', ApproveRCC.as_view(), name='approve_rcc_inspection'),
    path('ac-distribution-board/<uuid:pk>/approve/', ApproveACDistributionBoard.as_view(), name='approve_ac_distribution_board_inspection'),
    path('aux-transformer/<uuid:pk>/approve/', ApproveAUXTransformer.as_view(), name='approve_aux_transformer_inspection'),
    path('busduct/<uuid:pk>/approve/', ApproveBusduct.as_view(), name='approve_busduct_inspection'),
    path('high-voltage-panel/<uuid:pk>/approve/', ApproveHighVoltagePanel.as_view(), name='approve_high_voltage_panel_inspection'),
    path('periphery-lighting/<uuid:pk>/approve/', ApprovePeripheryLighting.as_view(), name='approve_periphery_lighting_inspection'),
    path('plumbing/<uuid:pk>/approve/', ApprovePlumbing.as_view(), name='approve_plumbing_inspection'),
    path('scada-system/<uuid:pk>/approve/', ApproveScadaSystem.as_view(), name='approve_scada_system_inspection'),
    path('wms/<uuid:pk>/approve/', ApproveWMS.as_view(), name='approve_wms_inspection'),
    path('plant-boundary-and-fencing/<uuid:pk>/approve/', ApprovePlantBoundaryAndFencing.as_view(), name='approve_plant_boundary_and_fencing'),
    path('chain-link-fencing/<uuid:pk>/approve/', ApproveChainLinkFencing.as_view(), name='approve_chain_link_fencing'),
    path('potential-transformer/<uuid:pk>/approve/', ApprovePotentialTransformer.as_view(), name='approve_potential_transformer_inspection'),
    path('battery-bank-and-battery-charger/<uuid:pk>/approve/', ApproveBatteryBankAndBatteryCharger.as_view(), name='approve_battery_bank_and_battery_charger_inspection'),
    path('control-cable-laying/<uuid:pk>/approve/', ApproveControlCableLaying.as_view(), name='approve_control_cable_laying_inspection'),
    path('fire-alarm-panel/<uuid:pk>/approve/', ApproveFireAlarmPanel.as_view(), name='approve_fire_alarm_panel_inspection'),
    path('inverter/<uuid:pk>/approve/', ApproveInverter.as_view(), name='approve_inverter_inspection'),
    path('string-cables/<uuid:pk>/approve/', ApproveStringCables.as_view(), name='approve_string_cables_inspection'),
    path('lightning-arrester/<uuid:pk>/approve/', ApproveLightningArrester.as_view(), name='approve_lightning_arrester_inspection'),
    path('string-cables2/<uuid:pk>/approve/', ApproveStringCables2.as_view(), name='approve_string_cables2_inspection'),

    # 2 witness
    path('dcdb/<uuid:pk>/approve/', ApproveDCDB.as_view(), name='approve_dcdb_inspection'), 
    path('outdoor-isolator-or-earth-switch/<uuid:pk>/approve/', ApproveOutdoorIsolatorOrEarthSwitch.as_view(), name='outdoor_isolator_or_earth_switch'), 
    path('transmission-lines/<uuid:pk>/approve/', ApproveTransmissionLines.as_view(), name='transmission_lines'), 
    path('inverter-or-control-room-building/<uuid:pk>/approve/', ApproveInverterOrControlRoomBuilding.as_view(), name='inverter_room_or_control_room'),

    # Complex checklists
    path('inverter-duty-transformer/<uuid:pk>/approve/', ApproveInverterDutyTransformer.as_view(), name='approve_inverter_duty_transformer_inspection'),
    path('spv-modules/<uuid:pk>/approve/', ApproveSPVModules.as_view(), name='approve_spv_modules_inspection'),

    # Complex forms
    path('earthing-system/<uuid:pk>/approve/', ApproveEarthingSystem.as_view(), name='approve_earthing_system_inspection'),
    path('ht-cable-pre-com/<uuid:pk>/approve/', ApproveHTCablePreCom.as_view(), name='approve_ht_cable_pre_comm_inspection'),
] + router.urls

