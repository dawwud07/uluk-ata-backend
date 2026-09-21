from django.contrib import admin
from .models import User , OTPCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _




@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_("Personal info"), {'fields': ('first_name', 'last_name', 'phone', 'avatar', 'date_of_birth')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups", 
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email","usable_password" ,  "password1", "password2"),
                
            },
        ),
    )
    
    ordering = ("email" , )
    
admin.site.register(OTPCode)