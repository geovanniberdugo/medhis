from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _lazy
from django.contrib.postgres import fields
from .managers import FormatoManager, HistoriaManager


class Formato(models.Model):
    """Modelo que guarda el formato de las historias clinicas de los pacientes."""

    nombre = models.CharField(_lazy('nombre'), max_length=100)
    contenido = fields.JSONField()
    valores_por_defecto = fields.JSONField(default=dict)
    activo = models.BooleanField(default=True)
    permiso = models.CharField(
        _lazy('permiso'), max_length=100,
        help_text=_lazy('Permiso que indica si el usuario puede usar este formato para crear registros en la historia')
    )
    diagnostico = models.BooleanField(_lazy('genera diagnostico'), default=False)

    objects = FormatoManager()

    class Meta:
        verbose_name = 'formato'
        verbose_name_plural = 'formatos'
        permissions = [
            ('can_add_triage', 'Puede agregar triage'),
            ('can_add_goniometria', 'Puede agregar goniometria'),
            ('can_add_recetario_umri', 'Puede agregar recetario umri'),
            ('can_add_consentimiento', 'Puede agregar consentimiento'),
            ('can_add_terapia_fisica', 'Puede agregar terapia fisica'),
            ('can_add_historia_clinica', 'Puede agregar historia clinica'),
            ('can_add_terapia_lenguaje', 'Puede agregar terapia lenguaje'),
            ('can_add_nota_enfermeria', 'Puede agregar nota de enfermeria'),
            ('can_add_historia_escaneada', 'Puede agregar historia escaneada'),
            ('can_add_terapia_ocupacional', 'Puede agregar terapia ocupacional'),
            ('can_add_terapia_respiratoria', 'Puede agregar terapia respiratoria'),
            ('can_add_historia_nutricional', 'Puede agregar historia nutricional'),
            ('can_add_solicitud_documento', 'Puede agregar solicitud de documento'),
            ('can_add_formato_fonoaudiologia', 'Puede agregar formato de fonoaudiologia'),
            ('can_add_historia_clinica_estetica', 'Puede agregar historia clinica estetica'),
            ('can_add_formato_electromiografia', 'Puede agregar formato de electromiografia'),
            ('can_add_historia_clinica_traccion', 'Puede agregar historia clinica de traccion'),
            ('can_add_historia_clinica_fisiatria', 'Puede agregar historia clinica de fisiatria'),
            ('can_add_historia_drenaje_linfatico', 'Puede agregar historia de drenaje linfatico'),
            ('can_add_historia_clinica_psicologica', 'Puede agregar historia clinica psicologica'),
            ('can_add_formato_bloqueo_infiltracion', 'Puede agregar formato de bloqueo e infiltracion'),
            ('can_add_historia_clinica_estetica_corporal', 'Puede agregar historia clinica estetica corporal'),
        ]
    
    def __str__(self):
        return self.nombre


class Historia(models.Model):
    """Modelo que guarda la información de los encuentros de un paciente con un proveedor."""

    fecha = models.DateTimeField(_lazy('fecha'), auto_now_add=True)
    formato = models.ForeignKey(Formato, related_name='encuentros', verbose_name=_lazy('formato'))
    cita = models.ForeignKey('agenda.Cita', related_name='encuentros', verbose_name=_lazy('cita'))
    proveedor = models.ForeignKey('organizacional.Empleado', related_name='historias', verbose_name=_lazy('medico'))
    contenido = fields.JSONField()
    data = fields.JSONField()
    terminada = models.BooleanField(default=False)

    objects = HistoriaManager()

    class Meta:
        verbose_name = 'historia'
        verbose_name_plural = 'historias'
        ordering = ['-fecha']
        permissions = [
            ('puede_ver_historias', 'Puede ver historias'),
            ('puede_agregar_triage', 'Puede agregar triage'),
            ('puede_editar_historias', 'Puede editar historias'),
            ('puede_imprimir_historias', 'Puede imprimir historias'),
            ('can_see_historias', 'Puede ver historias de un paciente'),
            ('can_edit_historias', 'Puede editar historias de un paciente'),
            ('can_delete_historias', 'Puede eliminar historias de un paciente'),
            ('can_abrir_historias', 'Puede abrir historias despues de cerradas'),
        ]
    
    def __str__(self):
        return '{0} - {1}'.format(self.pk, self.cita)
    
    def get_absolute_url(self):
        return reverse('historias:detail', kwargs={'pk': self.pk})
    
    @property
    def paciente(self):
        """:returns: Paciente asociado a la historia."""

        return self.cita.paciente
    
    @property
    def diagnostico(self):
        """Diagnostico formulado en la historia."""

        return self.data['rips']
    
    def can_edit(self, user):
        """Indica si el usuario puede editar el encuentro."""

        if user.has_perm('historias.puede_editar_historias'):
            return True

        if user.empleado.id == self.proveedor_id and not self.terminada:
            return True
        
        return False
    
    def can_delete(self, user):
        """Indica si el usuario puede borrar el encuentro."""
        
        if user.has_perm('historias.can_delete_historias'):
            return True

        if user.empleado.id == self.proveedor_id and not self.terminada:
            return True

        return False
    
    def can_abrir(self, user):
        return self.terminada and user.has_perm('historias.can_abrir_historias')
    
    def adjuntos_url(self):
        """URL de archivos adjuntos."""

        return reverse('historias:adjuntos', kwargs={'pk': self.pk})

    def visita_url(self):
        """URL de la visita asociada al encuentro."""

        return reverse('pacientes:historias-sesion', kwargs={'pk': self.cita_id})
    
    def print_url(self):
        """URL para la impresión del encuentro."""

        if self.terminada:
            return reverse('historias:print', kwargs={'pk': self.id})
        
        return None
    
    def abrir(self):
        self.terminada = False
        self.save()


def archivo_adjunto_path(instance, filename):
    """Path para el archivo adjunto."""
    
    return 'historia_{0}/adjuntos/{1}'.format(instance.historia_id, filename)


class Adjunto(models.Model):
    """Modelo que guarda los archivos adjuntos de una historia clinica."""

    archivo = models.FileField(upload_to=archivo_adjunto_path, verbose_name=_lazy('archivo'))
    historia = models.ForeignKey(Historia, related_name='adjuntos', verbose_name=_lazy('historia'))

    class Meta:
        verbose_name = 'adjunto'
        verbose_name_plural = 'adjuntos'
    

    def __str__(self):
        return '{0} - {1}'.format(self.historia, self.pk)

    def encounter_url(self):
        return reverse('historias:detail', kwargs={'pk': self.historia_id})

    def delete(self, *args, **kwargs):
        import os

        path = self.archivo.path
        super().delete(*args, **kwargs)
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)
