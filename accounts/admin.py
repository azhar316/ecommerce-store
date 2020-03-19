from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):

    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('email', 'admin', 'staff', 'is_active', )
    list_filter = ('email', 'admin', 'staff', 'is_active', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'staff', 'admin')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)
