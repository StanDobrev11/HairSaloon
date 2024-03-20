from datetime import datetime, timedelta

from django.core.exceptions import ValidationError


def open_hour_validator(value):
    time_str = '10:00'
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    if value <= time_obj:
        raise ValidationError('We are not opened at that hour. Please choose another date/time')


def close_hour_validator(value):
    time_str = '17:30'
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    if value >= time_obj:
        raise ValidationError('The saloon is closing ... please choose a different date/time')
