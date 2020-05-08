from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
import json

register = template.Library()

@register.filter(name='minutes')
def get_minutes(timedelta):
    return timedelta.seconds%3600//60


@register.filter(name='hours')
def get_hours(timedelta):
    return timedelta.seconds//3600



