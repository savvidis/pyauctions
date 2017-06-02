# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import *
from crispy_forms.layout import Layout, Field
from datetime import datetime, timedelta
from random import randint

register = template.Library()


@register.filter
def format_currency(value):
    try:
        return "€ {:,.0f}".format(value)
    except:
        return None


@register.filter
def divide(value, arg):
    print(value, arg)
    try:
        return int(value) / int(arg)
    except:
        pass
    else:
        return 0


@register.filter
def days_left(value):
    try:
        diff = value - datetime.today().date()
        return diff.days
    except:
        return None


@register.filter
def ifexists(value):
    if value:
        return value
    else:
        return ""


@register.filter
def random(v):
    return randint(1, 5)
