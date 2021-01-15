from django.conf import settings
from django.contrib.auth import get_user_model

def permiso_administrativo(request):
    """Indica si el usuario tiene permiso para ver el menu de utilidades."""

    has_permission = False
    MODELS = [
        ('servicios', 'plan'),
        ('servicios', 'tarifa'),
        ('servicios', 'cliente'),
        ('servicios', 'servicio'),
        ('organizacional', 'empleado'),
        ('organizacional', 'sucursal'),
        ('organizacional', 'institucion'), 
    ]

    if hasattr(request, 'user'):
        user = request.user
        sin_can = any(user.has_perm('{}.add_{}'.format(model[0], model[1])) for model in MODELS)
        con_can = any(user.has_perm('{}.can_add_{}'.format(model[0], model[1])) for model in MODELS)
        has_permission = sin_can or con_can
    
    return {
        'ANALYTICS': settings.ANALYTICS,
        'tiene_permiso_administrativo': has_permission
    }
