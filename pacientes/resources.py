from import_export import resources
from import_export.fields import Field
from . import models

class PacienteResource(resources.ModelResource):

    nombres = Field(attribute='nombres')

    class Meta:
        skip_unchanged = True
        report_skipped = True
        model = models.Paciente
        import_id_fields = ['numero_documento']
        fields = [
            'numero_documento', 'primer_apellido', 'segundo_apellido', 'telefono', 'direccion',
            'fecha_nacimiento', 'tipo_documento', 'genero', 'estado_civil', 'zona'
        ]
    
    def before_import_row(self, row, **kwargs):
        row['telefono'] = str(row['telefono']).split('-')[0].strip() or ''
        row['direccion'] = row['direccion'] or ''
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        nombres = instance.nombres.split()
        instance.primer_nombre = nombres[0]
        instance.segundo_nombre = ' '.join(nombres[1:])