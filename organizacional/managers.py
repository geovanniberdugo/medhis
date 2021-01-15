from django.db import models, transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class EmpleadoQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo empleado."""

    def medicos(self):
        """
        :returns:
            Un queryset con los empleados que son de tipo medico.
        """

        return self.filter(tipo=self.model.MEDICO)
    
    def by_sucursal(self, sucursal):
        """Filtra los empleados por sucursal."""

        return self.filter(horarios_atencion__sucursal=sucursal).distinct()

class EmpleadoManager(models.Manager.from_queryset(EmpleadoQuerySet)):
    """Manager personalizado para el modelo Empleado."""

    @transaction.atomic
    def crear_empleado_administrativo(self, username, password, rol, **kwargs):
        """Permite crear un empleado administrativo"""

        user = User.objects.create_user(username=username, password=password)
        user.groups.add(rol)
        return self.create(tipo=self.model.ADMINISTRATIVO, usuario=user, **kwargs)
    
    @transaction.atomic
    def crear_medico(self, username, password, rol, instituciones, **kwargs):
        """Permite crear un empleado administrativo"""

        user = User.objects.create_user(username=username, password=password)
        user.groups.add(rol)
        medico = self.create(tipo=self.model.MEDICO, usuario=user, **kwargs)
        medico.instituciones.set(instituciones)
        return medico


class HorarioAtencionQuerySet(models.QuerySet):
    """QuerySet personalizado para el modelo HorarioAtencion."""

    def by_sucursal(self, sucursal):
        """Filtra los horarios por sucursal."""

        return self.filter(sucursal=sucursal)
    
    def by_fecha(self, fecha):
        """Filtra los horarios por el dia de la fecha."""

        return self.filter(dia=fecha.weekday() + 1)
    
    def by_fechas(self, fechas):
        """Filtra los horarios por multiples fechas."""

        dias = map(lambda f: f.weekday() + 1, fechas)
        return self.filter(dia__in=dias)
    
    def by_dia(self, dia):
        """Filtra los horarios segun el dia."""

        return self.filter(dia=dia)

class HorarioAtencionManager(models.Manager.from_queryset(HorarioAtencionQuerySet)):
    """Manager personalizado para el modelo HorarioAtencion."""

    pass