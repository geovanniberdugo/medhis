from import_export.formats.base_formats import DEFAULT_FORMATS, XLSX
from django.core.management.base import BaseCommand, CommandError
from pacientes.resources import PacienteResource

class Command(BaseCommand):
    help = 'Importación de pacientes'

    def add_arguments(self, parser):
        parser.add_argument('file', help='Ruta del archivo xlsx')

    def handle(self, *args, **options):
        data = open(options['file'], mode='rb').read()
        dataset = XLSX().create_dataset(data)
        resource = PacienteResource()

        result = resource.import_data(dataset, dry_run=True)
        if not result.has_errors() and not result.has_validation_errors():
            result = resource.import_data(dataset, dry_run=False)
            self.stdout.write(self.style.SUCCESS('Done importing!!'))
            print(result.totals)
        else:
            self.stdout.write(self.style.ERROR('Errors while importing!!'))
            if result.has_errors():
                self.stdout.write(self.style.ERROR('........ has errors ..........'))
                print([error.error for error in result.base_errors])
            else:
                self.stdout.write(self.style.ERROR('........ has validation errors ..........'))
                print([(row.number, row.field_specific_errors, row.non_field_specific_errors) for row in result.invalid_rows])