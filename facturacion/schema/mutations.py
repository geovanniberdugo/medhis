import graphene
from graphene_django_extras import DjangoSerializerMutation, DjangoInputObjectType
from .. import serializers

class AnularFacturaInput(DjangoInputObjectType):

    razon_anulacion = graphene.String(required=True)

    class Meta:
        input_for = 'update'
        model = serializers.AnularFacturaSerializer.Meta.model
        only_fields = serializers.AnularFacturaSerializer.Meta.fields

class AnularFacturaMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        serializer_class = serializers.AnularFacturaSerializer
        only_fields = serializers.AnularFacturaSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class ReciboCajaMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'recibo_caja'
        serializer_class = serializers.ReciboCajaSerializer
        only_fields = serializers.ReciboCajaSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class AnularReciboCajaInput(DjangoInputObjectType):

    razon_anulacion = graphene.String(required=True)

    class Meta:
        input_for = 'update'
        model = serializers.AnularReciboCajaSerializer.Meta.model
        only_fields = serializers.AnularReciboCajaSerializer.Meta.fields

class AnularReciboCajaMutation(DjangoSerializerMutation):

    class Meta:
        input_field_name = 'input'
        output_field_name = 'recibo_caja'
        serializer_class = serializers.AnularReciboCajaSerializer
        only_fields = serializers.AnularReciboCajaSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class DetalleCajaInput(DjangoInputObjectType):

    class Meta:
        model = serializers.DetalleCajaSerializer.Meta.model
        only_fields = serializers.DetalleCajaSerializer.Meta.fields
        description = 'Input para guardar el detalle de la caja'

class CajaInput(DjangoInputObjectType):

    detalles = graphene.List(DetalleCajaInput, required=True)

    class Meta:
        model = serializers.CajaSerializer.Meta.model
        only_fields = serializers.CajaSerializer.Meta.fields
        description = 'Input para cerrar una caja'

class CajaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.CajaSerializer
        input_field_name = 'input'
        only_fields = serializers.CajaSerializer.Meta.fields
    
    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class EditCajaInput(DjangoInputObjectType):

    detalles = graphene.List(DetalleCajaInput, required=True)

    class Meta:
        model = serializers.EditarCajaSerializer.Meta.model
        only_fields = serializers.EditarCajaSerializer.Meta.fields
        description = 'Input para editar una caja'
        input_for = 'update'

class EditarCajaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.EditarCajaSerializer
        input_field_name = 'input'
        only_fields = serializers.EditarCajaSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class RecibirCajaInput(DjangoInputObjectType):

    class Meta:
        model = serializers.RecibirCajaSerializer.Meta.model
        only_fields = serializers.RecibirCajaSerializer.Meta.fields
        input_for = 'update'

class RecibirCajaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.RecibirCajaSerializer
        input_field_name = 'input'
        only_fields = serializers.RecibirCajaSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class VerificarCajaInput(DjangoInputObjectType):

    class Meta:
        model = serializers.VerificarCajaSerializer.Meta.model
        only_fields = serializers.VerificarCajaSerializer.Meta.fields
        input_for = 'update'

class VerificarCajaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.VerificarCajaSerializer
        input_field_name = 'input'
        only_fields = serializers.VerificarCajaSerializer.Meta.fields

    @classmethod
    def get_serializer_kwargs(cls, root, info, **kwargs):
        return {'context': {'request': info.context}}

class DetalleFacturaInput(DjangoInputObjectType):

    class Meta:
        model = serializers.DetalleFacturaSerializer.Meta.model
        only_fields = serializers.DetalleFacturaSerializer.Meta.fields
        description = 'Input para generar en detalle de una factura'

class FacturaInput(DjangoInputObjectType):

    detalle = graphene.List(DetalleFacturaInput, required=True)

    class Meta:
        model = serializers.FacturaSerializer.Meta.model
        only_fields = serializers.FacturaSerializer.Meta.fields
        description = 'Input para generar una factura'

class FacturaMutation(DjangoSerializerMutation):

    class Meta:
        serializer_class = serializers.FacturaSerializer
        input_field_name = 'input'
        only_fields = serializers.FacturaSerializer.Meta.fields

class Mutation:
    recibir_caja = RecibirCajaMutation.UpdateField(description='Recibe el dinero y lo verifica con respecto a lo ingresado en la caja')
    verificar_caja = VerificarCajaMutation.UpdateField(description='Verifica los recibos de caja con respecto a la caja')
    anular_recibo_caja = AnularReciboCajaMutation.UpdateField(description='Anular recibo de caja')
    crear_recibo_caja = ReciboCajaMutation.CreateField(description='Crea un recibo de caja')
    eliminar_factura = FacturaMutation.DeleteField(description='Eliminar una factura')
    anular_factura = AnularFacturaMutation.UpdateField(description='Anular factura')
    generar_factura = FacturaMutation.CreateField(description='Genera una factura')
    editar_caja = EditarCajaMutation.UpdateField(description='Editar caja')
    cerrar_caja = CajaMutation.CreateField(description='Cerrar caja')
