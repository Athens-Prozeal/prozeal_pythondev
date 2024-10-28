from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

from authentication.models import WorkSite
from authentication.permissions import is_sub_contractor, is_epc_admin_or_epc, is_client

User = get_user_model()

class BasePermitToWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    permit_no = models.CharField(max_length=255, unique=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    validity = models.DateTimeField()
    submitted_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='submitted_ptws')
    submitted_datetime = models.DateTimeField(auto_now_add=True)
    submitted_by_signature = models.ImageField(upload_to='ptw/signatures/')
    verified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='verified_ptws', blank=True, null=True)
    verified_datetime = models.DateTimeField(blank=True, null=True)
    verified_by_signature = models.ImageField(upload_to='ptw/signatures/', blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accepted_ptws', blank=True, null=True)
    approved_datetime = models.DateTimeField(blank=True, null=True)
    approved_by_signature = models.ImageField(upload_to='ptw/signatures/', blank=True, null=True)
    rejected_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rejected_ptws', blank=True, null=True)
    rejected_remark = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=255, choices=(
        ('submitted', 'Submitted'), # Submitted by sub-contractor
        ('epc_approved', 'EPC Approved'),
        ('client_approved', 'Client Approved'), # Open PTW
        ('client_rejected', 'Client Rejected'),
        ('closed', 'Closed'),
        ('auto_closed', 'Auto Closed'),
        ('expired', 'Expired')
    ), default='submitted')
    
    closure_requested_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='closure_request_ptws', blank=True, null=True)
    closure_requested_at = models.DateTimeField(blank=True, null=True)
    closure_accepted_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='closure_accepted_ptws', blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_%(class)s_ptws')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_%(class)s_ptws')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    @property
    def closure_requested(self):
        return self.closure_requested_by is not None

    def __str__(self):
        return f"{self.permit_no}"
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self._state.adding: # Checks for edit operation
            existing_ptw = self.__class__.objects.get(pk=self.pk)
            if self.work_site != existing_ptw.work_site:
                raise ValidationError('Cannot update the work site.')
            
        else: # Create operation
            self.permit_no = f"PTW-{uuid.uuid4().hex[:8].upper()}"

            # Validity should be a future date
            if self.validity < timezone.now():
                raise ValidationError('Validity should be a future date.')

        if not is_sub_contractor(self.submitted_by, self.work_site):
            raise ValidationError('Only sub-contractors users can submit PTWs.')

        if self.verified_by:
            if not is_epc_admin_or_epc(self.verified_by, self.work_site):
                raise ValidationError('Only EPC users can approve PTWs.')
            if not self.verified_datetime:
                raise ValidationError('Verified datetime is required.')
            if not self.verified_by_signature:
                raise ValidationError('Verified by signature is required.')

        if self.approved_by:
            if not is_client(self.approved_by, self.work_site):
                raise ValidationError('Only Client users can approve PTWs.')
            if not self.approved_datetime:
                raise ValidationError('Approved datetime is required.')
            if not self.approved_by_signature:
                raise ValidationError('Approved by signature is required.')

        if self.closure_requested_by and self.closure_requested_at is None:
            raise ValidationError('Closure requested at is required.')
        
        if self.closure_accepted_by and self.closed_at is None:
            raise ValidationError('Closed at is required.')

        super().save(*args, **kwargs)


class General(BasePermitToWork):
    section = models.CharField(max_length=155)
    lock_out_no = models.CharField(max_length=155)
    location = models.CharField(max_length=155)
    work_order_no = models.CharField(max_length=155)
    job_description = models.TextField()
    issued_to = models.CharField(max_length=155)

    # Following safety measures taken to carry out work
    tool_box_talk = models.CharField(max_length=255, choices=(
        ('yes', 'Yes'),
        ('no', 'No'),
        ('n/a', 'N/A')
    ))
    underground_or_overhead_cables_checked = models.CharField(max_length=255, 
         verbose_name='Underground or overhead cables checked for intervention', 
        choices=(
        ('yes', 'Yes'),
        ('no', 'No'),
        ('n/a', 'N/A')
    ))
    ppe_required_to_be_used = models.JSONField()
    other_work_permit_issued_same_location_datetime = models.BooleanField()
    other_permit_no = models.CharField(max_length=155, blank=True, null=True)
    any_other_safety_precaution_required = models.TextField(blank=True, null=True, verbose_name='Any other safety precaution required?')
    
    site_safety_induction = models.JSONField(blank=True, null=True)

    @property
    def table_identifier(self):
        return 'general'

    def save(self, *args, **kwargs):
        if self.other_work_permit_issued_same_location_datetime and not self.other_permit_no:
            raise ValidationError('Other permit number is required.')

        return super().save(*args, **kwargs)

