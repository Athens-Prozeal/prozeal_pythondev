from django.contrib import admin
from .models import (Excavation, AntiTermiteTreatment, 
PourCardForColumnConcrete, PourCardForSlabConcrete,
PlainCementConcreteWork,
HTCable, HighVoltagePanel, Inverter, StringCables, ScadaSystem, NIFPS,
TransmissionLines
)

class InspectionAdmin(admin.ModelAdmin):
    list_filter = ('approval_status', 'work_site') 

admin.site.register(Excavation, InspectionAdmin)
admin.site.register(AntiTermiteTreatment, InspectionAdmin)
admin.site.register(PourCardForColumnConcrete, InspectionAdmin)
admin.site.register(PourCardForSlabConcrete, InspectionAdmin)
admin.site.register(PlainCementConcreteWork, InspectionAdmin)
admin.site.register(HTCable, InspectionAdmin)
admin.site.register(HighVoltagePanel, InspectionAdmin)
admin.site.register(Inverter, InspectionAdmin)
admin.site.register(StringCables, InspectionAdmin)
admin.site.register(ScadaSystem, InspectionAdmin)
admin.site.register(NIFPS, InspectionAdmin)
admin.site.register(TransmissionLines)

