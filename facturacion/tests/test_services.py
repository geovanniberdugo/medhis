import pytest
import datetime
from freezegun import freeze_time
from django_dynamic_fixture import G, F, P
from common.tests.base import BaseTestCase
from organizacional.models import Empleado
from ..models import Factura, DetalleFactura, ParametroFacturaSiigo
from agenda.models import Cita
from .. import services as s

class AnularFacturaTest(BaseTestCase):

    @freeze_time("2019-11-11")
    def test_anular_factura(self):
        factura = G(Factura)
        empleado = G(Empleado)

        razon = 'probando anulacion'
        s.anular_factura(factura, razon, empleado)

        assert factura.razon_anulacion == razon
        assert factura.anulado_por_id == empleado.id
        assert factura.anulado_el == datetime.date(2019, 11, 11)

    @freeze_time("2019-11-11")
    def test_anular_factura_habilita_citas_facturar(self):
        factura = G(Factura)
        empleado = G(Empleado)
        detalle = G(DetalleFactura, factura=factura)
        cita1 = G(Cita, detalle_factura=detalle)
        cita2 = G(Cita, detalle_factura=detalle)

        razon = 'probando anulacion'
        s.anular_factura(factura, razon, empleado)

        cita1.refresh_from_db()
        cita2.refresh_from_db()
        detalle.refresh_from_db()
        assert cita1.detalle_factura == None
        assert cita2.detalle_factura == None
        assert sorted(detalle.citas_anuladas) == sorted([cita1.id, cita2.id])
