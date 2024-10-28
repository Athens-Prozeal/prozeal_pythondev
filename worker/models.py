from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import uuid
from django_countries.fields import CountryField

from .validators import validate_worker_age
from authentication.models import WorkSite
from authentication.permissions import has_work_site_role

User = get_user_model()

class Worker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    created_under = models.ForeignKey(User, on_delete=models.PROTECT, related_name='workers') # The user that the worker is created under
    induction_date = models.DateField()
    name = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to='worker/profile_pictures/', blank=True, null=True)
    father_name = models.CharField(max_length=150)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_worker_age])
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    designation = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15)
    emergency_contact_number = models.CharField(max_length=15)
    identity_marks = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=150)   
    state = models.CharField(max_length=150)
    country = CountryField()
    pincode = models.CharField(max_length=15)
    medical_fitness = models.ImageField(upload_to='medical_fitness/')
    aadhar = models.ImageField(upload_to='adhaar/') 
  
    # Additional fields
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_workers')
    last_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='last_updated_workers')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self._state.adding: # Check for edit operation
            existing_manpower = Worker.objects.get(pk=self.pk)
            if self.work_site != existing_manpower.work_site:
                raise ValidationError('Cannot update the work site.')
    
        if not has_work_site_role(self.created_under, self.work_site.id):
            raise IntegrityError('The user must have a role in the work site to create a worker under ')
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

