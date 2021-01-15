import waffle
from datetime import time
from .logging import logger
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied

class IPAccessMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        check_ip_acces = request.user.is_authenticated and not request.user.has_perm('organizacional.can_ingresar_sin_restriccion') and waffle.switch_is_active('ip_access')
        if check_ip_acces:
            ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
            if not ip:
                ip = request.META.get('REMOTE_ADDR')

            logger.warning('.................. ip middleware ........... {}'.format(ip))
            valid_ip = ip in settings.VALID_IPS
            if not valid_ip:
                raise PermissionDenied

        return self.get_response(request)

class TimeBasedAccessMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        check_time_access = request.user.is_authenticated and not request.user.has_perm('organizacional.can_ingresar_sin_restriccion') and waffle.switch_is_active('time_based_access')
        if check_time_access:
            now = timezone.localtime(timezone.now())

            logger.warning('.................. time based middleware ........... {}'.format(now))
            after_hours = time(now.hour, now.minute) < time(6, 0) or time(now.hour, now.minute) > time(19, 0)
            if after_hours:
                raise PermissionDenied

        return self.get_response(request)

