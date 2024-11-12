from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid

from authentication.models import WorkSite

User = get_user_model()

class ToolBoxTalk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    topic = models.CharField(max_length=255)
    date = models.DateField() # Date of the toolbox talk --> User selected
    number_of_participants = models.PositiveIntegerField()
    agency_name = models.CharField(max_length=255)
    evidence = models.ImageField(upload_to='evidence_uploads/')
    attendance = models.ImageField(upload_to='attendance/')

    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_tbts')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_tbts')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Toolbox Talk on {self.topic} by {self.agency_name}"

    def save(self, *args, **kwargs):
        if not self._state.adding: # Check for edit operation
            existing_toolboxtalk = ToolBoxTalk.objects.get(pk=self.pk)
            if self.work_site != existing_toolboxtalk.work_site:
                raise ValidationError('Cannot update the work site.')
            
        super().save(*args, **kwargs)

