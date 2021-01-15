from common.tests.base import BaseTestCase
from ..models import Empleado
from . import factories as fac

class EmpleadoManagerTest(BaseTestCase):
    """Pruebas unitarias para el manager del modelo Empleado."""

    def test_medicos_queryset(self):
        """Prueba que el queryset medicos devuelva solo los empleados que son medicos."""

        medico = fac.EmpleadoFactory(medico=True)
        no_medico = fac.EmpleadoFactory()

        medicos = Empleado.objects.medicos()
        self.assertIn(medico, medicos)
        self.assertNotIn(no_medico, medicos)