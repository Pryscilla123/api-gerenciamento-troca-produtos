from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from base_app.models import User


class UserAdmin(DefaultUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'cpf', 'telefone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Nível de Acesso', {'fields': ('nivel_acesso', )}),
        ('Aprovado', {'fields': ('aprovado', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'cpf', 'telefone', 'nivel_acesso', 'aprovado')}
         ),
    )


admin.site.register(User, UserAdmin)
