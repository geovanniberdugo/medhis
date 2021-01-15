import pytest
from unittest import mock
from django.contrib.auth import get_user_model
from common.tests.base import BaseTestCase
from organizacional.models import Empleado
from django_dynamic_fixture import G, N, F
from ..models import Historia

User = get_user_model()

def test_historia_print_url_returns_None_if_not_terminada():
    historia = Historia(terminada=False)
    assert historia.print_url() == None

def test_historia_print_url_not_returns_None_if_terminada():
    historia = Historia(terminada=True, id=2)
    assert historia.print_url() != None

def test_historia_can_delete_user_has_delete_permission_return_true():
    mock_user = mock.create_autospec(User, instance=True)
    mock_user.has_perm.return_value = True
    historia = Historia()

    assert historia.can_delete(mock_user)
    mock_user.has_perm.assert_called_once_with('historias.can_delete_historias')

def test_historia_can_abrir_historia_user_has_edit_permission_y_historia_cerrada_returns_true():
    mock_user = mock.create_autospec(User, instance=True)
    mock_user.has_perm.return_value = True
    historia = Historia(terminada=True)

    assert historia.can_abrir(mock_user)
    mock_user.has_perm.assert_called_once_with('historias.can_abrir_historias')

@mock.patch('historias.models.Historia.save', autospec=True)
def test_abrir_historia_marks_terminada_false(mock_save):
    historia = Historia(terminada=True)

    historia.abrir()
    assert historia.terminada == False
    mock_save.assert_called_once()
