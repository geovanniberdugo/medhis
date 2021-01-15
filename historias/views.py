from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from rest_framework import generics
from agenda.models import Cita
from .models import Historia, Formato, Adjunto
from .utils import flatten_medical_record
from . import serializers


class DetailHistoriaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    template_name = 'historias/detail_historia.html'
    permission_required = 'historias.puede_ver_historias'
    queryset = Historia.objects.all()


class PrintHistoriaView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    
    template_name = 'historias/print_historia.html'
    permission_required = 'historias.puede_imprimir_historias'
    queryset = Historia.objects.select_related('formato', 'proveedor', 'cita', 'cita__servicio_prestado__servicio').all()
    
    def get_context_data(self, **kwargs):
        data = flatten_medical_record(
            self.object.contenido, self.object.data,
            self.object.formato.diagnostico, self.object.cita.servicio
        )
        paciente = self.object.paciente
        kwargs.update({
            'content': data,
            'polymer3': True,
            'paciente': paciente,
            'edad': paciente.edad_relativa(self.object.cita.inicio.date()),
        })
        return super().get_context_data(**kwargs)


class NewEncounterAdjuntosView(generics.CreateAPIView):
    serializer_class = serializers.AdjuntoSerializer

    def get_sesion(self, pk):
        self.sesion = get_object_or_404(Cita, pk=pk)

    def get_formato(self, pk):
        self.formato = get_object_or_404(Formato, pk=pk)
    
    def get_proveedor(self, user):
        self.proveedor = user.empleado
    
    def create_encounter(self, formato, sesion, proveedor):
        return Historia.objects.create_encounter(formato, sesion, proveedor, {})
    
    def post(self, request, sesion, formato, *args, **kwargs):
        self.get_sesion(sesion)
        self.get_formato(formato)
        self.get_proveedor(request.user)
        return super().post(request, *args, **kwargs)
    
    @transaction.atomic()
    def perform_create(self, serializer):
        encounter = self.create_encounter(self.formato, self.sesion, self.proveedor)
        serializer.save(historia=encounter)

class AdjuntosEncuentroView(generics.ListCreateAPIView):
    serializer_class = serializers.AdjuntoSerializer

    def get_encounter(self, pk):
        self.encounter = get_object_or_404(Historia, pk=pk)
    
    def get(self, request, pk, *args, **kwargs):
        self.get_encounter(pk)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        self.get_encounter(pk)
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return self.encounter.adjuntos.all()
    
    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save(historia=self.encounter)

class FormatoView(generics.ListCreateAPIView):

    serializer_class = serializers.FormatoSerializer
    queryset = Formato.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class HistoriaView(generics.ListCreateAPIView):

    serializer_class = serializers.HistoriaSerializer
    queryset = Historia.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class AdjuntosHistoriaDestroyView(generics.DestroyAPIView):
    queryset = Adjunto.objects.all()
