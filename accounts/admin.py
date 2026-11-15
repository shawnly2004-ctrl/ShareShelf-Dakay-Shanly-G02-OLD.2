from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'account_type', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('ShareShelf', {'fields': ('role', 'account_type', 'contact_number',
                                   'barangay', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ShareShelf', {'fields': ('email', 'role', 'account_type')}),
    )

admin.site.register(User, CustomUserAdmin)