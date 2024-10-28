from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid

from authentication.models import WorkSite, Department, CorrectiveActionUser

User = get_user_model()

class ObservationClassification(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name
    

class SafetyObservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    reported_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='safety_observations_reported_by')
    date = models.DateField() # Date of the observation
    time = models.TimeField() # Time of the observation
    work_location = models.CharField(max_length=155)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    activity_performed = models.TextField()
    sub_contractor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='safety_observations_sub_contractor')
    safety_observation_found = models.TextField()
    type_of_observation = models.CharField(max_length=155, choices=((
        ('unsafe_act', 'Unsafe Act'),
        ('unsafe_condition', 'Unsafe Condition'),
    )))
    classification = models.CharField(max_length=155) # From classification model
    risk_rated = models.CharField(max_length=155, choices=(('high', 'High'), ('significant', 'Significant'), ('medium', 'Medium'), ('low', 'Low')))
    corrective_action_required = models.TextField(null=True, blank=True)
    corrective_action_taken = models.TextField(null=True, blank=True)
    corrective_action_assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='safety_observations_corrective_action_assigned_to')
    observation_status = models.CharField(max_length=155, choices=(('open', 'Open'), ('closed', 'Closed'), ('expired', 'Expired')))
    closed_on = models.DateField(null=True, blank=True)
    before_image = models.ImageField(upload_to='safety_observation')
    after_image = models.ImageField(upload_to='safety_observation', null=True, blank=True)
    remarks = models.TextField()
    status = models.CharField(max_length=25, choices=(
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('verification_required', 'Verification Required'),
    ))

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_safety_observations')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_safety_observations')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.date} - {self.work_location} - '

    def save(self, *args, **kwargs):
        if not self._state.adding: # edit operation
            existing_toolboxtalk = SafetyObservation.objects.get(pk=self.pk)
            if self.work_site != existing_toolboxtalk.work_site:
                raise ValidationError('Cannot update the work site.')
            
        if self.department not in self.reported_by.departments.all():
            raise ValidationError('Invalid Department') 
            
        if self.corrective_action_assigned_to not in CorrectiveActionUser.objects.get(work_site=self.work_site).users.all():
            raise ValidationError('Invalid Corrective Action User')
        
        if self.reported_by == self.corrective_action_assigned_to:
            raise ValidationError('Reported by and Corrective Action Assigned to should be different')

        if self.observation_status == 'closed' :
            if self.status != 'closed':
                raise ValidationError('Status should be closed for closed observation')

            if not self.closed_on:
                raise ValidationError('Closed on date is required for closed observation')
    
            if not self.after_image:
                raise ValidationError('After image is required for closed observation')

            if not self.corrective_action_taken:
                raise ValidationError('Corrective Action Taken is required for open observation')
        
        if self.observation_status == 'open':
            if self.status not in ('open', 'verification_required'):
                raise ValidationError('Status should be open or verification required for open observation')
    
        super().save(*args, **kwargs)

