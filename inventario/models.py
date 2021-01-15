from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

class Medicamento(models.Model):
    codigo_atc = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200, blank=True)
    nombre = models.CharField(max_length=200)
    concentracion = models.ManyToManyField('inventario.Concentracion', through='inventario.PrincipioActivo', related_name='concentracion')
    forma_farmaceutica = models.ManyToManyField('inventario.FormaFarmaceutica', through='inventario.PrincipioActivo', related_name='forma_farmaceutica')

    def __str__(self):
        return self.nombre

class PrincipioActivo(models.Model):
    concentracion = models.ForeignKey('inventario.Concentracion', related_name='principios_activos')
    medicamento = models.ForeignKey('inventario.Medicamento', related_name='principios_activos')
    forma_farmaceutica = models.ForeignKey('inventario.FormaFarmaceutica', related_name='principios_activos')

    def __str__(self):
        return '{} - {} - {}'.format(self.medicamento, self.concentracion, self.forma_farmaceutica)

class Concentracion(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class FormaFarmaceutica(models.Model):
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):

    MEDICAMENTO = '1'
    DISPOSITIVOS = '2'
    PRODUCTO_FACIAL = '3'

    TIPOS = (
        (MEDICAMENTO, _lazy('Medicamento')),
        (DISPOSITIVOS, _lazy('Dispositivos')),
        (PRODUCTO_FACIAL, _lazy('Producto Facial')),
    )

    tipo = models.CharField(max_length=1, default=MEDICAMENTO, choices=TIPOS)
    nombre = models.CharField(max_length=200, blank=True)
    principio_activo = models.ForeignKey('inventario.PrincipioActivo', related_name='productos')
    registro_invima = models.CharField(max_length=200, blank=True)
    laboratorio = models.ForeignKey('inventario.Laboratorio', related_name='productos', null=True)
    unidad_medida = models.ForeignKey('inventario.Unidad', related_name='productos', null=True)

    def __str__(self):
        return '{} - {}'.format(self.nombre, self.principio_activo)

class Inventario(models.Model):
    producto = models.ForeignKey('inventario.Producto', related_name='inventario')
    lote = models.CharField(max_length=200, blank=True)
    fecha_entrada = models.DateField()
    cantidad = models.IntegerField()
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return '{}'.format(self.producto)

class Laboratorio(models.Model):
    nit = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    tipo = models.ForeignKey('inventario.TipoDeMovimiento', related_name='movimientos')
    fecha = models.DateField()
    factura = models.CharField(max_length=50, blank=True)
    inventario = models.ForeignKey('inventario.Inventario', related_name='movimientos')
    cantidad = models.IntegerField()
    observacion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.tipo, self.inventario)

class TipoDeMovimiento(models.Model):
    ENTRADA = '1'
    SALIDA = '2'
    TRASLADO = '3'

    TIPOS = (
        (ENTRADA, _lazy('Entrada')),
        (SALIDA, _lazy('Salida')),
        (TRASLADO, _lazy('Traslado')),
    )

    clase = models.CharField(max_length=1, default=ENTRADA, choices=TIPOS)
    descripcion = models.CharField(max_length=100)
    detalle = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.clase, self.descripcion)
