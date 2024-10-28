from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid

from authentication.models import WorkSite
from authentication.permissions import has_work_site_role

User = get_user_model()


class AbstractInspectionChecklist3W(models.Model):
    """ For checklist inspections. Used for both category checlist and naked checklist inspections having 3 witness """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APPROVAL_STATUS_CHOICES = (
        ('initiated', 'Initiated'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved')
    )
    
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    checked_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_checked_by')
    checked_by_date = models.DateField(auto_now_add=True)
    witness_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_witness_1')
    witness_1_date = models.DateField(blank=True, null=True)
    witness_1_signature = models.ImageField(upload_to='inspection/signatures/', blank=True, null=True)
    witness_1_approved = models.BooleanField(default=False)

    witness_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_witness_2')
    witness_2_date = models.DateField(blank=True, null=True)
    witness_2_signature = models.ImageField(upload_to='inspection/signatures/', blank=True, null=True)
    witness_2_approved = models.BooleanField(default=False)

    witness_3 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_witness_3')
    witness_3_date = models.DateField(blank=True, null=True)
    witness_3_signature = models.ImageField(upload_to='inspection/signatures/', blank=True, null=True)
    witness_3_approved = models.BooleanField(default=False)

    approval_status = models.CharField(choices=APPROVAL_STATUS_CHOICES, max_length=15, default='initiated')

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)s')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_%(class)s')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self._state.adding: # Checks for edit operation
            existing_inspection = self.__class__.objects.get(pk=self.pk)
            if self.work_site != existing_inspection.work_site:
                raise ValidationError('Cannot update the work site.')
            
            if existing_inspection.approval_status == 'approved':
                raise ValidationError('Cannot update an approved inspection.')
            
        if self.checked_by == self.witness_1 or self.checked_by == self.witness_2 or self.checked_by == self.witness_3:
            raise ValidationError('Witness cannot be same as checked by.')
        
        if self.witness_1 == self.witness_2 or self.witness_1 == self.witness_3 or self.witness_2 == self.witness_3:
            raise ValidationError('Witnesses cannot be same.')

        # Check if all witnesses have approved to mark the inspection as approved  
        if self.approval_status == 'approved':
            if not self.witness_1_approved or not self.witness_2_approved or not self.witness_3_approved:
                raise ValidationError('Cannot approve without all witnesses approval.')
        
        if not has_work_site_role(self.checked_by, self.work_site):
            raise IntegrityError('Provided Checked by must have a role for the provided work site.')

        if not has_work_site_role(self.witness_1, self.work_site) or not has_work_site_role(self.witness_2, self.work_site) or not has_work_site_role(self.witness_3, self.work_site):
            raise IntegrityError('Provided Witness must have a role for the provided work site.')

        # Check if date is provided for witness approval
        if self.witness_1_approved and not self.witness_1_date:
            raise ValidationError('Witness 1 approval date is required.')
        
        if self.witness_2_approved and not self.witness_2_date:
            raise ValidationError('Witness 2 approval date is required.')
        
        if self.witness_3_approved and not self.witness_3_date:
            raise ValidationError('Witness 3 approval date is required.')

        super().save(*args, **kwargs)

    
    @property
    def is_approved(self):
        return self.approval_status == 'approved'

    class Meta:
        abstract = True


class AbstractInspectionChecklist2W(models.Model):
    """ For checklist inspections. Used for both category checlist and naked checklist inspections having 2 witnesses """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    APPROVAL_STATUS_CHOICES = (
        ('initiated', 'Initiated'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved')
    )
    
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    checked_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_checked_by')
    checked_by_date = models.DateField(auto_now_add=True)
    witness_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_witness_1')
    witness_1_date = models.DateField(blank=True, null=True)
    witness_1_signature = models.ImageField(upload_to='inspection/signatures/', blank=True, null=True)
    witness_1_approved = models.BooleanField(default=False)

    witness_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_witness_2')
    witness_2_date = models.DateField(blank=True, null=True)
    witness_2_signature = models.ImageField(upload_to='inspection/signatures/', blank=True, null=True)
    witness_2_approved = models.BooleanField(default=False)

    approval_status = models.CharField(choices=APPROVAL_STATUS_CHOICES, max_length=15, default='initiated')

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)s')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_%(class)s')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self._state.adding: # Checks for edit operation
            existing_inspection = self.__class__.objects.get(pk=self.pk)
            if self.work_site != existing_inspection.work_site:
                raise ValidationError('Cannot update the work site.')
            
            if existing_inspection.approval_status == 'approved':
                raise ValidationError('Cannot update an approved inspection.')
            
        if self.checked_by == self.witness_1 or self.checked_by == self.witness_2:
            raise ValidationError('Witness cannot be same as checked by.')
        
        if self.witness_1 == self.witness_2:
            raise ValidationError('Witnesses cannot be same.')


        # Check if all witnesses have approved to mark the inspection as approved  
        if self.approval_status == 'approved':
            if not self.witness_1_approved or not self.witness_2_approved:
                raise ValidationError('Cannot approve without all witnesses approval.')
        

        # Check selected user have role in work site
        if not has_work_site_role(self.checked_by, self.work_site):
            raise IntegrityError('Provided Checked by must have a role for the provided work site.')

        if not has_work_site_role(self.witness_1, self.work_site) or not has_work_site_role(self.witness_2, self.work_site):
            raise IntegrityError('Provided Witness must have a role for the provided work site.')


        # Check if date is provided for witness approval
        if self.witness_1_approved and not self.witness_1_date:
            raise ValidationError('Witness 1 approval date is required.')
        
        if self.witness_2_approved and not self.witness_2_date:
            raise ValidationError('Witness 2 approval date is required.')
        
        super().save(*args, **kwargs)
        

    @property
    def is_approved(self):
        return self.approval_status == 'approved'

    class Meta:
        abstract = True


# Checklist for Excavation 004
class Excavation(AbstractInspectionChecklist3W): 
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    checklists = models.JSONField() 

    @property
    def table_identifier(self):
        return 'excavation'

    def __str__(self):
        return f'{self.ref_drawing_no}'


# Installation checklist for Anti-termite Treatment 020
class AntiTermiteTreatment(AbstractInspectionChecklist3W): 
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    grade_of_concrete = models.CharField(max_length=155)
    source_of_concrete = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'anti-termite-treatment'

    def __str__(self):
        return f'{self.ref_drawing_no}'


# Check List/Pour Card For Column Concrete 006
class PourCardForColumnConcrete(AbstractInspectionChecklist3W):
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    grade_of_concrete = models.CharField(max_length=155)
    source_of_concrete = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'pour-card-for-column-concrete'

    def __str__(self):
        return f'{self.ref_drawing_no}'


# Check List/Pour Card for Slab Concrete 009
class PourCardForSlabConcrete(AbstractInspectionChecklist3W):
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    grade_of_concrete = models.CharField(max_length=155)
    source_of_concrete = models.CharField(max_length=155)
    level = models.CharField(max_length=155)
    checklists = models.JSONField()    
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'pour-card-for-slab-concrete'
    
    def __str__(self):
        return f'{self.ref_drawing_no}'


# Check List / Pour Card For Plinth Beam/Lintel Beam/Roof Beam 007
class PourCardForBeam(AbstractInspectionChecklist3W): 
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    grade_of_concrete = models.CharField(max_length=155)
    source_of_concrete = models.CharField(max_length=155)
    level = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'pour-card-for-beam'

    def __str__(self):
        return f'{self.ref_drawing_no}'
    

# Check List for Plain Cement Concrete Work 010
class PlainCementConcreteWork(AbstractInspectionChecklist3W):
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    grade_or_mix_proportion_of_concrete = models.CharField(max_length=155)
    source_of_concrete = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'plain-cement-concrete-work'

    def __str__(self):
        return f'{self.ref_drawing_no}'
    

# Check List for Plastering 011
class Plastering(AbstractInspectionChecklist3W):
    project_name = models.CharField(max_length=155)
    description = models.TextField()
    date_of_checking = models.DateField()
    ref_drawing_no = models.CharField(max_length=155)
    checklists = models.JSONField() 

    @property
    def table_identifier(self):
        return 'plastering'

    def __str__(self):
        return f'{self.ref_drawing_no}'



# Un Grouped 
# INSTALLATION CHECKLIST FOR HT CABLE 054
class HTCable(AbstractInspectionChecklist3W):
    site_location_or_area = models.CharField(max_length=155)
    drawing_or_specification_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'ht-cable'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR CCTV INSTALLATION 084
class CCTVInstallation(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'cctv-installation'
    
    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# CHECKLIST FOR CULVERT WORK 021
class CulvertWork(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'culvert-work'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECKLIST FOR REMOTE TERMINAL UNIT 087
class RemoteTerminalUnit(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'remote-terminal-unit'
    
    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECKLIST FOR UPS 088
class UPS(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'ups'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECK LIST ICOG PANEL 042
class ICOGPanel(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'icog-panel'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# Installation Checklist for Painting 022
class Painting(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'painting'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# CHECKLIST FOR RCC 012
class RCC(AbstractInspectionChecklist3W):
    project_name = models.CharField(max_length=155)
    customer = models.CharField(max_length=155)
    location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField()
    remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'rcc'
    
    def __str__(self):
        return f'{self.project_name}'


# INSTALLATION CHECKLIST FOR AC DISTRIBUTION BOARD 026
class ACDistributionBoard(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'ac-distribution-board'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR AUX TRANSFORMER 081
class AUXTransformer(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'aux-transformer'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR BUSDUCT 083
class Busduct(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'busduct'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECK LIST HIGH VOLTAGE PANEL 043
class HighVoltagePanel(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'high-voltage-panel'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR PERIPHERY LIGHTING 086
class PeripheryLighting(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    block_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'periphery-lighting'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# Installation Checklist for Plumbing 023
class Plumbing(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'plumbing'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR SCADA SYSTEM 055
class ScadaSystem(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'scada-system'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR WMS 059
class WMS(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'wms'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# CHECKLIST FOR PLANT BOUNDARY AND FENCING (RCC)
class PlantBoundaryAndFencing(AbstractInspectionChecklist3W):
    project_name_and_capacity = models.CharField(max_length=155)
    client_name = models.CharField(max_length=155)
    epc_contractor_name = models.CharField(max_length=155)
    date = models.DateField()
    consultant_name = models.CharField(max_length=155)
    location_or_area = models.CharField(max_length=155)
    contractor_name = models.CharField(max_length=155)
    work_supervisor_name = models.CharField(max_length=155)
    any_other_observation = models.TextField()
    checklists = models.JSONField() 

    @property
    def table_identifier(self):
        return 'plant-boundary-and-fencing'

    def __str__(self):
        return f'{self.project_name_and_capacity}'
    

# CHECKLIST FOR PLANT BOUNDARY AND FENCING Chain-Link Fencing 019
class ChainLinkFencing(AbstractInspectionChecklist3W):
    project_name_and_capacity = models.CharField(max_length=155)
    client_name = models.CharField(max_length=155)
    epc_contractor_name = models.CharField(max_length=155)
    date = models.DateField()
    consultant_name = models.CharField(max_length=155)
    location_or_area = models.CharField(max_length=155)
    drawing_no = models.CharField(max_length=155)
    contractor_name = models.CharField(max_length=155)
    work_supervisor_name = models.CharField(max_length=155)
    any_other_observation = models.TextField()
    checklists = models.JSONField() 

    @property
    def table_identifier(self):
        return 'chain-link-fencing'

    def __str__(self):
        return f'{self.project_name_and_capacity}'


# INSTALLATION CHECKLIST FOR POTENTIAL TRANSFORMER 073
class PotentialTransformer(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'potential-transformer'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECKLIST FOR BATTERY BANK & BATTERY CHARGER 082
class BatteryBankAndBatteryCharger(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'battery-bank-and-battery-charger'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR CONTROL CABLE LAYING 034
class ControlCableLaying(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'control-cable-laying'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR FIRE ALARM PANEL 085
class FireAlarmPanel(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'fire-alarm-panel'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR INVERTER 044
class Inverter(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'inverter'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECKLIST FOR STRING CABLES 045
class StringCables(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'string-cables'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'


# INSTALLATION CHECKLIST FOR LIGHTNING ARRESTER 058
class LightningArrester(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'lightning-arrester'

    def __str__(self):
        return f'{self.drawing_or_specification_no}'
    

# INSTALLATION CHECK LIST FOR STRING CABLES 056
class StringCables2(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)    
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'string-cables2'
    
    def __str__(self):
        return self.drawing_or_specification_no   


# INSTALLATION CHECKLIST FOR NIFPS 057
class NIFPS(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments = models.TextField()

    @property
    def table_identifier(self):
        return 'nifps'

    def __str__(self):
        return f'{self.drawing_or_specification_no}' 


# 2 witness
class DCDB(AbstractInspectionChecklist2W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'dcdb'
    
    def __str__(self):
        return self.drawing_or_specification_no


# INSTALLATION CHECKLIST FOR OUTDOOR ISOLATOR / EARTH SWITCH 072
class OutdoorIsolatorOrEarthSwitch(AbstractInspectionChecklist2W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)    
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'outdoor-isolator-or-earth-switch'
    
    def __str__(self):
        return self.drawing_or_specification_no


#  INSTALLATION CHECKLIST FOR TRANSMISSION LINES 099
class TransmissionLines(AbstractInspectionChecklist2W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)    
    checklists = models.JSONField() 
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'transmission-lines'
    
    def __str__(self):
        return self.drawing_or_specification_no    


# CHECK LIST FOR MODULE INTERCONNECTION 027
class ModuleInterconnection(AbstractInspectionChecklist2W):
    project_name = models.CharField(max_length=155)
    customer =  models.CharField(max_length=155)
    date = models.DateField()
    block_no =  models.CharField(max_length=155)
    drawing_no =  models.CharField(max_length=155)
    report_no =  models.CharField(max_length=155)
    row_from =  models.CharField(max_length=155)
    row_to =  models.CharField(max_length=155)
    structure_from = models.CharField(max_length=155)
    structure_to = models.CharField(max_length=155)
    checklists = models.JSONField() 
    remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'module-interconnection'
    
    def __str__(self):
        return self.project_name


# Check List for Inverter Room/Control Room Building Final Acceptance Checklist 016
class InverterOrControlRoomBuilding(AbstractInspectionChecklist2W):
    project_name = models.CharField(max_length=155)
    location_or_area = models.CharField(max_length=155)
    date_of_audit = models.DateField()
    checklists = models.JSONField()

    @property
    def table_identifier(self):
        return "inverter-or-control-room-building"

    def __str__(self):
        return self.project_name
    

# INSTALLATION CHECKLIST FOR INVERTER DUTY TRANSFORMER 036
class InverterDutyTransformer(AbstractInspectionChecklist3W):
    drawing_or_specification_no = models.CharField(max_length=155)
    serial_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'inverter-duty-transformer'
    
    def __str__(self):
        return self.drawing_or_specification_no


# INSTALLATION CHECKLIST FOR SPV MODULES 071
class SPVModules(AbstractInspectionChecklist2W):
    drawing_or_specification_no = models.CharField(max_length=155)
    site_location_or_area = models.CharField(max_length=155)
    checklists = models.JSONField()
    comments_or_remarks = models.TextField()

    @property
    def table_identifier(self):
        return 'spv-modules'
    
    def __str__(self):
        return self.drawing_or_specification_no


# Complex forms
# EARTHING SYSTEM 079
class EarthingSystem(AbstractInspectionChecklist3W):
    name_of_client = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    date_of_test = models.DateField()
    earth_tester_details = models.JSONField()
    observation_or_comments = models.TextField()

    @property
    def table_identifier(self):
        return 'earthing-system'

    def __str__(self):
        return self.name_of_client


# HT CABLE Pre-Commissioning Checklist 080
class HTCablePreCom(AbstractInspectionChecklist3W):
    name_of_client = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    date_of_test = models.DateField()
    make = models.CharField(max_length=155)
    cable_rating = models.CharField(max_length=155)
    data = models.JSONField()

    @property
    def table_identifier(self):
        return 'ht-cable-pre-com'
    
    def __str__(self):
        return self.name_of_client

