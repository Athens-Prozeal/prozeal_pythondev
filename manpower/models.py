from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model
import uuid

from authentication.models import WorkSite
from authentication.permissions import is_sub_contractor

User = get_user_model()

class Manpower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    date = models.DateField() # Date of the manpower report --> User selected
    number_of_workers = models.PositiveIntegerField()
    sub_contractor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='manpower_reports')

    VERIFICATION_STATUS_CHOICES = (
        ('Not Verified', 'Not Verified'),
        ('Verified', 'Verified'),
        ('Revise', 'Revise')
    )

    verification_status = models.CharField(max_length=25, choices=VERIFICATION_STATUS_CHOICES, default='Not Verified')
    verified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='verified_manpowers', null=True, blank=True)

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_manpowers')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='last_updated_manpowers')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['work_site', 'date', 'sub_contractor'], name='unique_manpower_report'),
        ]

    def save(self, *args, **kwargs):
        if not self._state.adding: # Check for edit operation
            existing_manpower = Manpower.objects.get(pk=self.pk)
            if self.work_site != existing_manpower.work_site:
                raise ValidationError('Cannot update the work site.')

        if not is_sub_contractor(self.sub_contractor, self.work_site.id):
            raise IntegrityError('Provided Sub Contractor must have a "Sub Contractor" role for the provided work site.')
        
        if self.verification_status == 'Verified' and self.verified_by is None:
            raise IntegrityError('Verified Manpower must have a verified_by field.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Manpower Report on {self.date} by {self.sub_contractor} "    
    
