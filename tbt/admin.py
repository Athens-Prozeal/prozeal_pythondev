from django.contrib import admin

from .models import ToolBoxTalk

@admin.register(ToolBoxTalk)
class ToolBoxTalkAdmin(admin.ModelAdmin):
    list_display = ('topic', 'work_site', 'date', 'number_of_participants', 'agency_name')
    list_filter = ('work_site', 'date', 'agency_name')
    search_fields = ('topic', 'agency_name')
    date_hierarchy = 'date'
    ordering = ('-date', )
    readonly_fields = ('created_at', 'last_updated_at', 'created_by', 'last_updated_by')
    fieldsets = (
        (None, {
            'fields': ('work_site', 'topic', 'date', 'number_of_participants', 'agency_name', 'evidence', 'attendance')
        }),
        ('Additional Information', {
            'fields': ('created_by', 'last_updated_by', 'created_at', 'last_updated_at',),
            'classes': ('collapse',)
        })
    )
    raw_id_fields = ('work_site', )

    def save_model(self, request, obj, form, change):
        if not change: # If the object is being created
            obj.created_by = request.user
        obj.last_updated_by = request.user
        super().save_model(request, obj, form, change)
