# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import *

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
