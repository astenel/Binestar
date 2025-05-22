# apps/clients/models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group, 
)

# apps/clients/models.py

from django.db import models

class Cliente(models.Model):
    id_cliente    = models.AutoField(primary_key=True)
    apellidos     = models.CharField(max_length=100)
    nombres       = models.CharField(max_length=100)
    ci            = models.CharField('cédula', max_length=20, unique=True)
    sexo          = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField()
    telefono      = models.CharField(max_length=15, blank=True, null=True)
    # …otros campos que tenga tu tabla Cliente…

    class Meta:
        db_table = 'Cliente'
        managed  = True   # o True si quieres que Django cree/gestione esa tabla

class UsuarioManager(BaseUserManager):
    """Manager para crear usuarios y superusuarios."""
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        # Usamos set_password para generar correctamente el hash
        user.set_password(password)
        # Lo guardamos en password_hash si quieres mantener ese campo:
        user.password_hash = user.password
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario     = models.AutoField(primary_key=True)
    username       = models.CharField('usuario', max_length=50, unique=True)
    password_hash  = models.CharField('hash de contraseña', max_length=255)
    email          = models.EmailField('correo electrónico', max_length=100)
    es_admin       = models.BooleanField('es admin', default=False)
    is_staff       = models.BooleanField('staff status', default=False)
    is_active      = models.BooleanField('activo', default=True)
    fecha_creacion = models.DateTimeField('fecha de creación', auto_now_add=True)

    # Ahora sí apunta a tu modelo Cliente recién definido:
    cliente = models.ForeignKey(
        Cliente,
        db_column='id_cliente',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    # Sobrescribimos groups y user_permissions para darles un related_name distinto
    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        related_name='clients_usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='permisos de usuario',
        blank=True,
        related_name='clients_usuario_permissions',
        related_query_name='usuario',
    )

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UsuarioManager()

    class Meta:
        db_table = 'Usuario'
        managed  = True  # o True si quieres que Django gestione la creación de la tabla

