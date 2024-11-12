from django.contrib import admin

from .models import Manpower

@admin.register(Manpower)
class ManpowerAdmin(admin.ModelAdmin):
    list_display = ('date', 'work_site', 'number_of_workers', 'sub_contractor', 'verification_status')
    list_filter = ('work_site', 'date', 'sub_contractor', 'verification_status')
    search_fields = ('work_site', 'sub_contractor')
    ordering = ('-date',)
    date_hierarchy = 'date'
    readonly_fields = ('verified_by', 'created_at', 'last_updated_at', 'created_by', 'last_updated_by')
    fieldsets = (
        (None, {
            'fields': ('date', 'work_site',  'number_of_workers', 'sub_contractor', 'verification_status')
        }),
        ('Additional Information', {
            'fields': ('verified_by', 'created_by', 'last_updated_by', 'created_at', 'last_updated_at',),
            'classes': ('collapse',)
        })
    )
    raw_id_fields = ('work_site', 'sub_contractor')

    def save_model(self, request, obj, form, change):
        if not change: # If the object is being created
            obj.created_by = request.user
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)

