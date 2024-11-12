from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "department"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser model.
    """
    email = models.EmailField(_("email address"), unique=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    departments = models.ManyToManyField(Department, blank=True)
    is_epc_admin = models.BooleanField(default=False) # Main admin (If EPC is Software purchaser)

    class Meta:
        db_table = "auth_user"

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.company})'


class WorkSite(models.Model):
    """
    Model to represent a worksite.
    """
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "worksite"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = slugify(self.name)

        super().save(*args, **kwargs)  
  
    def __str__(self):
        return self.name


class WorkSiteRole(models.Model):
    """
    Model to represent the role of a user at a worksite.
    """
    ROLE_CHOICES = (
        ("epc_admin", "EPC Admin"), # Dummy role for master admin
        ("epc", "EPC User"),
        ("client", "Client User"),
        ("sub_contractor", "Sub Contractor"),
        ("quality_inspector", "Quality Inspector"),
        ("safety_officer", "Safety Officer"),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="work_site_roles")
    work_site = models.ForeignKey(WorkSite, on_delete=models.PROTECT)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)    

    class Meta:
        db_table = "worksite_role"
        unique_together = ["user", "work_site"] # User cannot have more than one role at a worksite
    
    def __str__(self):
        return f"{self.user} - {self.work_site} - {self.role}"


class CorrectiveActionUser(models.Model):
    work_site = models.OneToOneField(WorkSite, on_delete=models.PROTECT, related_name="corrective_action_users")
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.work_site.name

