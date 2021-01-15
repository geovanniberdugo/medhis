from django.db import models

class Reporte(models.Model):

    class Meta:
        managed = False
        permissions = [
            ('can_see_relacion_facturas', 'Puede ver relacion de facturas'),
            ('can_see_citas_paciente', 'Puede ver reporte citas por paciente'),
            ('can_see_relacion_recibos_caja', 'Puede ver relacion recibos de caja'),
            ('can_see_asignacion_citas', 'Puede ver reporte de asignacion de citas'),
            ('can_see_citas_no_cumplidas', 'Puede ver reporte de citas no cumplidas'),
            ('can_see_certificado_asistencia', 'Puede ver certificado de asistencia'),
            ('can_see_medicos_ordenan_tratamiento', 'Puede ver reporte de medicos que ordenan tratamiento'),
            ('can_see_tratamientos_facturado_entidad', 'Puede ver reporte tratamientos facturados por entidad'),
            ('can_see_tratamientos_pago_profesional', 'Puede ver relacion de tratamientos para pago de profesional'),
            ('can_see_tratamientos_iniciados_profesional', 'Puede ver reporte tratamientos iniciados por profesional'),
            ('can_see_tratamientos_terminado_profesional', 'Puede ver reporte tratamientos terminados por profesional'),
            ('can_see_tratamientos_no_facturados_entidad', 'Puede ver reporte de tratamientos no facturados por entidad'),
            ('can_see_tratamientos_no_terminado_profesional', 'Puede ver reporte tratamientos no terminados por profesional'),
        ]
