from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from FonoAppAdministracion.queryset import FonoAPP_Queryset

class FonoApp_Administracion(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField("Codigo registro usuario", primary_key=True)
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    tipo = models.BooleanField(default=False) # 0 = vet / 1 = indep
    estado = models.BooleanField(default=True) # 1 = activo
    is_staff = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    last_conection = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rut']
    
    # Vinculación del QuerySet como Manager
    objects = FonoAPP_Queryset.as_manager()
    
    class Meta:
        db_table = 'FonoApp_Administracion'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.nombre} ({self.rut})'