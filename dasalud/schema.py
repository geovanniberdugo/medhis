import graphene
import common.schema
import agenda.schema
import globales.schema
import servicios.schema
import historias.schema
import pacientes.schema
import facturacion.schema
import organizacional.schema
import parametrizacion.schema
from graphene_django_extras import all_directives

class Query(
    parametrizacion.schema.Query,
    organizacional.schema.Query,
    facturacion.schema.Query,
    servicios.schema.Query,
    historias.schema.Query,
    pacientes.schema.Query,
    globales.schema.Query,
    agenda.schema.Query,
    common.schema.Query,
    graphene.ObjectType
):
    """Base entrypoint to the schema. Inherits from all other schemas."""

    pass


class Mutation(
    organizacional.schema.Mutation,
    facturacion.schema.Mutation,
    historias.schema.Mutation,
    servicios.schema.Mutation,
    pacientes.schema.Mutation,
    agenda.schema.Mutation,
    graphene.ObjectType
):
    """Base entry point for mutations. Inherits from all other mutations."""

    pass

schema = graphene.Schema(query=Query, mutation=Mutation, directives=all_directives)
