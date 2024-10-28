from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import WorkSite, WorkSiteRole, CorrectiveActionUser, Department


User = get_user_model()

admin.site.register(WorkSite)


class UserRoleFilter(admin.SimpleListFilter):
    title = _('User Role')
    parameter_name = 'user_role'

    def lookups(self, request, model_admin):
        return (
            ('epc', _('EPC')),
            ('client', _('Client')),
            ('sub_contractor', _('Sub Contractor')),
        )

    def queryset(self, request, queryset):
        work_site = request.GET.get('work_site')
        if self.value():
            if work_site:
                return queryset.filter(Q(work_site_roles__work_site=work_site) & Q(work_site_roles__role=self.value()))

            return queryset.filter(work_site_roles__role=self.value())
        return queryset

class WorkSiteFilter(admin.SimpleListFilter):
    title = _('Work Site')
    parameter_name = 'work_site'

    def lookups(self, request, model_admin):
        work_sites = WorkSite.objects.all()
        return [(work_site.id, work_site.name) for work_site in work_sites]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(work_site_roles__work_site=self.value()).distinct()
        return queryset

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_epc_admin', 'company')
    add_fieldsets = (
            (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'company'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'company', 'departments')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_epc_admin',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = (UserRoleFilter, WorkSiteFilter, 'is_staff', 'is_superuser', 'is_active', 'is_epc_admin', 'groups', 'company')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'company')


@admin.register(WorkSiteRole)
class WorkSiteRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'work_site', 'role')
    list_filter = ('work_site', 'role')
    search_fields = ('user__username', 'work_site__name')
    raw_id_fields = ('user', 'work_site')


admin.site.register(CorrectiveActionUser)
admin.site.register(Department)
