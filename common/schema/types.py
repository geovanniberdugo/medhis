import datetime
from django.utils import timezone
from graphene_django_extras.base_types import CustomDateTime, CustomDateFormat

class LocalCustomDateTime(CustomDateTime):
    @staticmethod
    def serialize(dt):
        if isinstance(dt, CustomDateFormat):
            return dt.date_str

        assert isinstance(
            dt, (datetime.datetime, datetime.date)
        ), ('Received not compatible datetime "{}"'.format(repr(dt)))
        return timezone.localtime(dt).isoformat()
