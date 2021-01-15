import pytest
from unittest import mock
from datetime import datetime
from django_dynamic_fixture import N, P, F
from ..models import Factura, ParametroFacturaSiigo
from ..siigo import write_to_excel, exportar_facturas


def test_write_to_excel():
    data = [
        ['F', 1, 1, '2345653423', 'D', 10000, 2019, 10, 10, 1, 1, 1, 1, 1, '890234432', '', 'desc', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, '', 0, 0, '', '', ''],
        ['F', 1, 1, '4105020411', 'C', 10000, 2019, 10, 10, 1, 1, 2, 1, 1, '890234432', '', 'desc', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, '', 0, 0, '', '', '']
    ]
    write_to_excel(data)

def test_write_to_excel_empty_list():
    write_to_excel([])

@pytest.mark.actual
def test_exportar_factura_sin_coopago_sin_iva():

    expected = [
        ['F', 1, 1, '2345653423', 'D', 10000, 2019, 10, 10, 1, 1, 0, 1, 0, 0, '890234432', 0, 'Factura 1', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 'F-001', 1, 1, 2019, 11, 30],
        ['F', 1, 1, '4105020411', 'C', 10000, 2019, 10, 10, 1, 1, 0, 2, 0, 0, '890234432', 0, 'Terapia M', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '700', '701', '701', 0, 0, 1, 0, 0, 0, 0, '', 0, 0, 0, 'F-001', 0, 0, '', '', '']
    ]

    factura = N(Factura, numero=1, fecha_expedicion=datetime(2019, 10, 10), cliente=F(puc_facturacion='2345653423', nit='890234432'), persist_dependencies=False)
    factura.total = lambda: 10000
    factura.subtotal = lambda: 10000
    factura.total_coopago = lambda: 0
    factura.puc_subtotal = lambda: '4105020411'
    factura.codigo_linea = lambda: '700'
    factura.codigo_producto = lambda: '701'
    factura.cuenta_siigo = mock.MagicMock()
    factura.cuenta_siigo().__str__.return_value = 'Terapia M'

    result = exportar_facturas([factura])
    assert result == expected

@pytest.mark.actual
def test_exportar_factura_con_coopago_sin_iva():
    expected = [
        ['F', 1, 1, '2345653423', 'D', 10000, 2019, 12, 10, 1, 1, 0, 1, 0, 0, '890234432', 0, 'Factura 1', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 'F-001', 1, 1, 2020, 1, 31],
        ['F', 1, 1, '4105020414', 'C', 20000, 2019, 12, 10, 1, 1, 0, 2, 0, 0, '890234432', 0, 'Terapia M', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '600', '601', '601', 0, 0, 1, 0, 0, 0, 0, '', 0, 0, 0, 'F-001', 0, 0, '', '', ''],
        ['F', 1, 1, '2805050402', 'D', 10000, 2019, 12, 10, 1, 1, 0, 3, 1, 0, '890234432', 0, 'Coopago', 0, 'N', 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 'N', '', '', '', '', '', 0, 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 'F-001', 0, 0, '', '', '']
    ]

    factura = N(Factura, numero=1, fecha_expedicion=datetime(2019, 12, 10), cliente=F(puc_facturacion='2345653423', nit='890234432'), persist_dependencies=False)
    factura.total = lambda: 10000
    factura.subtotal = lambda: 20000
    factura.total_coopago = lambda: 10000
    factura.puc_subtotal = lambda: '4105020414'
    factura.codigo_linea = lambda: '600'
    factura.codigo_producto = lambda: '601'
    factura.cuenta_siigo = mock.MagicMock()
    factura.cuenta_siigo().__str__.return_value = 'Terapia M'

    result = exportar_facturas([factura])
    assert result == expected
