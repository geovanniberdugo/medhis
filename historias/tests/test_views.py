from unittest import mock
from django.contrib.auth import get_user_model
from common.tests.base import BaseTestCase
from common.tests.factories import UsuarioFactory
from pacientes.tests.factories import ServicioRealizarFactory
from ..models import Historia

User = get_user_model()

class PrintHistoriaViewTest(BaseTestCase):

    URL = 'historias:print'
    PERMISSION = 'puede_imprimir_historias'

    def test_not_login_user_redirects_login_page(self):
        self.get(self.URL, pk=1)
        self.response_302()
    
    def test_user_dont_have_correct_permissions_returns_302(self):
        self.login(mock.create_autospec(User, instance=True))
        self.get(self.URL, pk=1)
        self.response_302()
    
    def test_user_with_correct_permission_but_historia_dont_exits_get_404(self):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL, pk=1)
        self.response_404()

    @mock.patch('historias.views.flatten_medical_record', autospec=True)
    @mock.patch('historias.views.DetailView.get_object', autospec=True, return_value=mock.create_autospec(Historia, instance=True))
    def test_user_with_permission_print_historia_get_200(self, mock_get_object, mock_flatten_medical_record):
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get_check_200(self.URL, pk=1)
    
    @mock.patch('historias.views.flatten_medical_record', autospec=True)
    @mock.patch('historias.views.DetailView.get_object', autospec=True)
    def test_user_with_permission_print_historia_calls_flatten(self, mock_get_object, mock_flatten_medical_record):
        mock_historia = mock.create_autospec(Historia, instance=True)
        mock_get_object.return_value = mock_historia
        self.login(UsuarioFactory(user_permissions=[self.PERMISSION]))
        self.get(self.URL, pk=1)
        mock_flatten_medical_record.assert_called_once_with(
            mock_historia.contenido,
            mock_historia.data,
            mock_historia.formato.diagnostico,
            mock_historia.cita.servicio
        )
    

class AdjuntosHistoriaViewTest(BaseTestCase):
    """Pruebas unitarias para la vista de adjuntos de una historia."""

    URL = 'historias:adjuntos'

    def setUp(self):
        self.login(UsuarioFactory())
    
    def test_get_servicio_no_existe_returns_404(self):
        """Prueba que si el servicio no existe devuelva un 404."""

        self.get(self.URL, 454)
        self.response_404()
    
    def test_post_servicio_no_existe_returns_404(self):
        """prueba que si el servicio no existe devuelva un 404."""

        self.post(self.URL, 343)
        self.response_404()
    
    def test_crear_adjunto(self):
        """Prueba que guarde el archivo adjunto."""

        data = {}
        servicio = ServicioRealizarFactory()
        self.post(self.URL, servicio.id, data=data, extra={'format': 'json'})
        # self.response_201() TODO probar que se suba el archivo
