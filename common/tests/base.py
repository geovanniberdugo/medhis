import json
from rest_framework.test import APIClient
from graphene_django.utils.testing import GraphQLTestCase
from tenant_schemas.test.cases import FastTenantTestCase
from tenant_schemas.test.client import TenantClient
from django.urls import reverse_lazy
from test_plus.test import TestCase
from dasalud.schema import schema


class BaseClient(TenantClient, APIClient):
    """Cliente base para las pruebas."""

    pass


class BaseTestCase(FastTenantTestCase, TestCase):
    """Clase base para pruebas unitarias."""

    def _pre_setup(self):
        super()._pre_setup()
        self.client = BaseClient(self.tenant)
    
    def login(self, usuario):
        self.client.login(username=usuario.username, password='adminadmin')

class BaseGraphTestCase(FastTenantTestCase, GraphQLTestCase):
    
    GRAPHQL_URL = reverse_lazy('common:graphql2')
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._client = BaseClient(cls.tenant)
    
    def format_response(self, resp):
        return json.loads(resp.content)
    
    def login(self, usuario):
        self._client.login(username=usuario.username, password='adminadmin')

