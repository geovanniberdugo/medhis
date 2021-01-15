def agenda(request):
    """Retorna un queryset con las agendas multiples como variable de contexto."""

    from .models import Agenda

    return {
        'agendas': Agenda.objects.all()
    }