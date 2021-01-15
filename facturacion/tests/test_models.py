import pytest
import datetime
from freezegun import freeze_time
from django_dynamic_fixture import G, F, P
from servicios.models import Cliente
from common.tests.base import BaseTestCase
from agenda.models import Cita
from organizacional.models import Empleado
from ..models import Factura, DetalleFactura, ParametroFacturaSiigo

class ParametroFacturaSiigoModelTest(BaseTestCase):

    def test_str(self):
        param = G(ParametroFacturaSiigo, tipo_servicio=F(nombre='Terapia'), tipo_cliente='MP')
        assert str(param) == 'Terapia Prepagada'

class FacturaModelTest(BaseTestCase):

    def test_puc_subtotal(self):
        CUENTA = '346546'
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))
        G(ParametroFacturaSiigo, tipo_servicio=F(id=3), tipo_cliente='MP', cuenta_puc=CUENTA)

        assert factura.puc_subtotal() == CUENTA

    def test_puc_subtotal_not_param(self):
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))

        assert factura.puc_subtotal() == ''

    def test_cuenta_siigo(self):
        CODIGO = '500'
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))
        param = G(ParametroFacturaSiigo, tipo_servicio=F(id=3), tipo_cliente='MP', codigo_linea=CODIGO)

        assert factura.cuenta_siigo() == param

    def test_codigo_linea(self):
        CODIGO = '500'
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))
        G(ParametroFacturaSiigo, tipo_servicio=F(id=3), tipo_cliente='MP', codigo_linea=CODIGO)

        assert factura.codigo_linea() == CODIGO

    def test_codigo_linea_not_param(self):
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))

        assert factura.codigo_linea() == ''
    
    def test_codigo_producto(self):
        CODIGO = '501'
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))
        G(ParametroFacturaSiigo, tipo_servicio=F(id=3), tipo_cliente='MP', codigo_producto=CODIGO)

        assert factura.codigo_producto() == CODIGO

    def test_codigo_producto(self):
        factura = G(Factura, cliente=F(tipo='MP'))
        detalle = G(DetalleFactura, factura=factura)
        G(Cita, detalle_factura=detalle, servicio_prestado=F(servicio=F(tipo=F(id=3))))

        assert factura.codigo_producto() == ''