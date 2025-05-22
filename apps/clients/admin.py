# apps/clients/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombres', 'apellidos', 'ci', 'sexo')
    search_fields = ('nombres', 'apellidos', 'ci')

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'is_staff', 'is_active', 'es_admin')
    list_filter  = ('is_staff', 'is_active', 'es_admin', 'groups')
    search_fields = ('username', 'email')
    ordering      = ('username',)

    # Estos campos no se pueden editar, solo mostrar
    readonly_fields = ('last_login', 'fecha_creacion')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email', 'cliente')}),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'es_admin',
                'groups', 'user_permissions'
            ),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_creacion')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'is_active', 'is_staff', 'es_admin'
            ),
        }),
    )
