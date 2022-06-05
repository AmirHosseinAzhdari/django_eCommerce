from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from .models import User, OtpCode


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name', 'mobile_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {"fields": ('email', 'mobile_number', 'full_name', 'password')}),
        ('Permissions', {"fields": ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {"fields": ('mobile_number', 'email', 'full_name', 'is_active', 'is_admin', 'password1', 'password2')}),
    )

    search_fields = ('email', 'full_name', 'mobile_number')
    ordering = ('-last_login',)
    filter_horizontal = ()


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'code', 'created')
    ordering = ("-created",)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
