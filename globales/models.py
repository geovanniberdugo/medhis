"""Estos modelos se manejan de manera global para todos los clientes."""

from django.utils.translation import ugettext_lazy as _lazy
from django.db import models
from .managers import CieManager, PobladoManager


class Profesion(models.Model):
    """Modelo para guardar las profesiones."""

    nombre = models.CharField(_lazy('nombre'), max_length=250)
    codigo = models.IntegerField(_lazy('código'))

    class Meta:
        verbose_name = 'profesión'
        verbose_name_plural = 'profesiones'
    
    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    """Modelo para guardar los departamentos."""

    codigo = models.CharField(_lazy('código'), max_length=2)
    nombre = models.CharField(_lazy('nombre'), max_length=250)

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
    
    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    """Modelo para guardar los municipios."""

    codigo = models.CharField(_lazy('código'), max_length=3)
    nombre = models.CharField(_lazy('nombre'), max_length=250)
    departamento = models.ForeignKey(Departamento, related_name='municipios', verbose_name=_lazy('departamento'))

    class Meta:
        verbose_name = 'municipio'
        verbose_name_plural = 'municipios'
    
    def __str__(self):
        return self.nombre


class Poblado(models.Model):
    """Modelo para guardar los poblados."""

    codigo = models.CharField(_lazy('código'), max_length=3)
    nombre = models.CharField(_lazy('nombre'), max_length=250)
    municipio = models.ForeignKey(Municipio, related_name='poblados', verbose_name=_lazy('municipio'))

    objects = PobladoManager()

    class Meta:
        verbose_name = 'poblado'
        verbose_name_plural = 'poblados'
    
    def __str__(self):
        return self.nombre


class Cie(models.Model):
    """Modelo que guarda los codigos internacionales de enfermedades usados en los RIPS de las historias clinicas."""

    codigo = models.CharField(_lazy('codigo'), max_length=4)
    nombre = models.CharField(_lazy('nombre'), max_length=400)

    objects = CieManager()

    class Meta:
        verbose_name = 'Cie'
        verbose_name_plural = 'Cies'
    
    def __str__(self):
        return '{} - {}'.format(self.codigo, self.nombre)
