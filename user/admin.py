from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from user.models import User


class UserAdmin(DjangoUserAdmin):
    """
    Defines the appearance and functionality of the User Model section of the Django Admin page
    """
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('email', 'first_name', 'last_name', 'is_vendor')
        }),
        ('Administrative', {
            'fields': ('password', 'last_login', 'date_joined', 'is_active')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'groups')
        }),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'is_vendor',
                'email',
                'password1',
                'password2'
            )}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
