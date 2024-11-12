from django.contrib import admin

from .models import ObservationClassification, SafetyObservation

admin.site.register(ObservationClassification)
admin.site.register(SafetyObservation)
