from django.contrib import admin

from .models import Worker

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'work_site', 'created_under', 'induction_date', 'father_name', 'gender', 'date_of_birth')
    list_filter = ('work_site', 'gender', 'blood_group')

    search_fields = ('name', 'father_name')
    readonly_fields = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')
    fieldsets = (
        (None, {
            'fields': ('work_site', 'created_under', 'induction_date', 'name', 'profile_pic','father_name', 'gender', 'date_of_birth', 'blood_group', 'mobile_number', 'emergency_contact_number', 'identity_marks', 'address', 'city', 'state', 'country', 'pincode', 'medical_fitness', 'aadhar',)
        }), 
        ('Additional Information', {
            'fields': ('created_by', 'last_updated_by', 'created_at', 'last_updated_at'),
            'classes': ('collapse',)
        }))  
    raw_id_fields = ('work_site', 'created_under')  

    def save_model(self, request, obj, form, change):
        if not change: # If the object is being created
            obj.created_by = request.user
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)
    
